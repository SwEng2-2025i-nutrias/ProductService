import os
import sys
import types

#Tener clara la estructura del proyecto y la ubicación de los módulos
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.insert(0, project_root)

# Provide dummy modules to avoid real DB, SQLAlchemy and repository imports
# Se generaron modules dummy para evitar la base de datos, SQLAlchemy y la importación
# Dummy flask_sqlalchemy
fake_fsa = types.ModuleType('flask_sqlalchemy')
fake_fsa.SQLAlchemy = lambda *args, **kwargs: None
sys.modules['flask_sqlalchemy'] = fake_fsa
# Dummy app.config.db
fake_db_mod = types.ModuleType('app.config.db')
fake_db_mod.db = None
sys.modules['app.config.db'] = fake_db_mod
# Dummy repository module before importing controller
fake_repo_mod = types.ModuleType('app.adapters.repository.sqlalchemy_product_repository')
class DummyRepo:
    pass
fake_repo_mod.SQLAlchemyProductRepository = DummyRepo
sys.modules['app.adapters.repository.sqlalchemy_product_repository'] = fake_repo_mod
# Dummy middleware module before importing controller
fake_mm_mod = types.ModuleType('app.adapters.middleware.auth_middleware')
class DummyAuthMiddleware:
    def require_auth(self, f): return f
fake_mm_mod.AuthMiddleware = DummyAuthMiddleware
sys.modules['app.adapters.middleware.auth_middleware'] = fake_mm_mod

import pytest
from flask import Flask, g
from datetime import datetime

# Import blueprint and use_case
from app.adapters.controller.product_controller import product_bp, use_case

# Dummy product for testing
class DummyProduct:
    def __init__(self, product_id, name, farm_id, type, quantity, price_per_unit, description, harvest_date):
        self.product_id = product_id
        self.name = name
        self.farm_id = farm_id
        self.type = type
        self.quantity = quantity
        self.price_per_unit = price_per_unit
        self.description = description
        self.harvest_date = harvest_date
    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "farm_id": self.farm_id,
            "type": self.type,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "description": self.description,
            "harvest_date": self.harvest_date.isoformat(),
            "created_at": datetime.now().isoformat()
        }

@pytest.fixture
def app(monkeypatch):
    app = Flask(__name__)
    # Disable auth requirement for testing
    monkeypatch.setattr("app.adapters.controller.product_controller.require_auth", lambda f: f)
    app.register_blueprint(product_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# ----------------------- Tests -----------------------
# GET /products

def test_get_all_products_success(client, monkeypatch):
    dummy = DummyProduct(1, "Apple", "farm1", "fruit", 10, 2.5, "Fresh", datetime(2022,1,1))
    monkeypatch.setattr(use_case, 'list_products', lambda: [dummy])
    res = client.get('/api/v1/products')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list) and data[0]['product_id'] == 1

# GET /products/me

def test_get_my_products_success(client, monkeypatch):
    dummy = DummyProduct(2, "Banana", "farm2", "fruit", 20, 1.0, "Yellow", datetime(2022,2,2))
    monkeypatch.setattr(use_case, 'get_products_by_farm', lambda farm_id: [dummy])
    @client.application.before_request
    def set_user():
        g.user_id = 'farm2'
    res = client.get('/api/v1/products/me')
    assert res.status_code == 200
    data = res.get_json()
    assert data['count'] == 1 and data['products'][0]['product_id'] == 2

# POST /products

def test_create_product_missing_fields(client):
    @client.application.before_request
    def set_user():
        g.user_id = 'farm1'
    res = client.post('/api/v1/products', json={})
    assert res.status_code == 400
    assert 'No data provided' in res.get_json()['error']

def test_create_product_success(client, monkeypatch):
    called = {}
    def fake_create(**kwargs):
        called.update(kwargs)
    monkeypatch.setattr(use_case, 'create_product', fake_create)
    @client.application.before_request
    def set_user():
        g.user_id = 'farm1'
    payload = {
        'name': 'Orange', 'type': 'fruit', 'quantity': 5,
        'price_per_unit': 3.0, 'description': 'Sweet'
    }
    res = client.post('/api/v1/products', json=payload)
    assert res.status_code == 201
    assert called['name'] == 'Orange' and called['farm_id'] == 'farm1'

# GET /products/<id>

def test_get_product_found(client, monkeypatch):
    dummy = DummyProduct(3, "Grapes", "farm3", "fruit", 15, 4.0, "Green", datetime(2022,3,3))
    monkeypatch.setattr(use_case, 'get_product', lambda id: dummy)
    res = client.get('/api/v1/products/3')
    assert res.status_code == 200
    assert res.get_json()['product_id'] == 3

def test_get_product_not_found(client, monkeypatch):
    monkeypatch.setattr(use_case, 'get_product', lambda id: None)
    res = client.get('/api/v1/products/99')
    assert res.status_code == 404
    assert res.get_json()['error'] == 'Product not found'

# PUT /products/<id>

def test_update_product_success(client, monkeypatch):
    existing = DummyProduct(4, "Pear", "farm4", "fruit", 8, 2.0, "Juicy", datetime(2022,4,4))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    monkeypatch.setattr(use_case, 'update_product_full', lambda **kwargs: True)
    @client.application.before_request
    def set_user():
        g.user_id = 'farm4'
    payload = {'name': 'Pear Updated', 'harvest_date': '2022-04-05T00:00:00Z'}
    res = client.put('/api/v1/products/4', json=payload)
    assert res.status_code == 200
    assert res.get_json()['message'] == 'Product updated'

def test_update_product_forbidden(client, monkeypatch):
    existing = DummyProduct(5, "Kiwi", "farm5", "fruit", 5, 3.5, "Tasty", datetime(2022,5,5))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    @client.application.before_request
    def set_user():
        g.user_id = 'other_farm'
    res = client.put('/api/v1/products/5', json={'name': 'Nope'})
    assert res.status_code == 403
    assert 'No tienes permisos' in res.get_json()['error']

def test_update_product_invalid_date(client, monkeypatch):
    existing = DummyProduct(6, "Melon", "farm6", "fruit", 3, 5.0, "Sweet", datetime(2022,6,6))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    @client.application.before_request
    def set_user():
        g.user_id = 'farm6'
    res = client.put('/api/v1/products/6', json={'harvest_date': 'invalid-date'})
    assert res.status_code == 400
    assert 'Invalid harvest_date format' in res.get_json()['error']

# PATCH /products/<id>

def test_patch_product_success(client, monkeypatch):
    existing = DummyProduct(7, "Mango", "farm7", "fruit", 12, 2.2, "Ripe", datetime(2022,7,7))
    updated = DummyProduct(7, "Mango Ripe", "farm7", "fruit", 12, 2.2, "Ripe", datetime(2022,7,7))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    monkeypatch.setattr(use_case, 'patch_product', lambda id, data: updated)
    @client.application.before_request
    def set_user():
        g.user_id = 'farm7'
    res = client.patch('/api/v1/products/7', json={'name': 'Mango Ripe'})
    assert res.status_code == 200
    body = res.get_json()
    assert body['product']['name'] == 'Mango Ripe'

def test_patch_product_not_found(client, monkeypatch):
    monkeypatch.setattr(use_case, 'get_product', lambda id: None)
    @client.application.before_request
    def set_user():
        g.user_id = 'farmX'
    res = client.patch('/api/v1/products/999', json={'name': 'X'})
    assert res.status_code == 404

def test_patch_product_forbidden(client, monkeypatch):
    existing = DummyProduct(8, "Plum", "farm8", "fruit", 6, 1.5, "Plumsy", datetime(2022,8,8))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    @client.application.before_request
    def set_user():
        g.user_id = 'other'
    res = client.patch('/api/v1/products/8', json={'description': 'Nope'})
    assert res.status_code == 403

def test_patch_product_no_fields(client, monkeypatch):
    existing = DummyProduct(9, "Cherry", "farm9", "fruit", 30, 0.5, "Cherries", datetime(2022,9,9))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    @client.application.before_request
    def set_user():
        g.user_id = 'farm9'
    res = client.patch('/api/v1/products/9', json={})
    assert res.status_code == 400
    assert 'No data provided' in res.get_json()['error']

def test_patch_product_invalid_value(client, monkeypatch):
    existing = DummyProduct(10, "Berry", "farm10", "fruit", 7, 2.0, "Berry Good", datetime(2022,10,10))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    def raise_value(id, data):
        raise ValueError("Bad patch")
    monkeypatch.setattr(use_case, 'patch_product', raise_value)
    @client.application.before_request
    def set_user():
        g.user_id = 'farm10'
    res = client.patch('/api/v1/products/10', json={'quantity': -1})
    assert res.status_code == 400
    assert 'Bad patch' in res.get_json()['error']

# DELETE /products/<id>

def test_delete_product_success(client, monkeypatch):
    existing = DummyProduct(11, "Fig", "farm11", "fruit", 4, 3.3, "Figgy", datetime(2022,11,11))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    monkeypatch.setattr(use_case, 'delete_product', lambda id: True)
    @client.application.before_request
    def set_user():
        g.user_id = 'farm11'
    res = client.delete('/api/v1/products/11')
    assert res.status_code == 200
    assert res.get_json()['message'] == 'Product deleted'

def test_delete_product_not_found(client, monkeypatch):
    monkeypatch.setattr(use_case, 'get_product', lambda id: None)
    @client.application.before_request
    def set_user():
        g.user_id = 'farmY'
    res = client.delete('/api/v1/products/999')
    assert res.status_code == 404

def test_delete_product_forbidden(client, monkeypatch):
    existing = DummyProduct(12, "Lemon", "farm12", "fruit", 9, 1.2, "Sour", datetime(2022,12,12))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    @client.application.before_request
    def set_user():
        g.user_id = 'other'
    res = client.delete('/api/v1/products/12')
    assert res.status_code == 403

def test_delete_product_failure(client, monkeypatch):
    existing = DummyProduct(13, "Peach", "farm13", "fruit", 2, 4.4, "Peachy", datetime(2022,1,13))
    monkeypatch.setattr(use_case, 'get_product', lambda id: existing)
    monkeypatch.setattr(use_case, 'delete_product', lambda id: False)
    @client.application.before_request
    def set_user():
        g.user_id = 'farm13'
    res = client.delete('/api/v1/products/13')
    assert res.status_code == 500
    assert 'Failed to delete product' in res.get_json()['error']
