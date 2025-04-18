# Here, we will register all our routes
from .budget_routes import budget_bp
from .transaction_routes import transaction_bp
from .budget_summary_routes import budget_summary_bp
from .category_summary_routes import category_summary_bp

def register_routes(app):
    app.register_blueprint(budget_bp, url_prefix='/api/budgets')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    app.register_blueprint(budget_summary_bp, url_prefix='/api/budget-summary')
    app.register_blueprint(category_summary_bp, url_prefix='/api/category-summary')