// product-service/main.cpp
#include "crow.h"
#include <pqxx/pqxx>
#include <cstdlib>
#include <sstream>
#include <vector>
#include <string>
#include <iomanip>

std::string format_price(double price) {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(2) << price;
    return oss.str();
}

// Helper: Get the database connection string from environment or default.
std::string get_db_conn_str() {
    const char* env_p = std::getenv("DATABASE_URL");
    if (env_p)
        return std::string(env_p);
    else
        return "dbname=ecommerce user=myuser password=mypassword host=postgres port=5432";
}

// Function to fetch all products from the DB.
crow::json::wvalue fetch_products() {
    crow::json::wvalue result;
    std::vector<crow::json::wvalue> productsList;
    try {
        pqxx::connection c(get_db_conn_str());
        pqxx::work txn(c);
        pqxx::result r = txn.exec("SELECT id, name, price FROM products ORDER BY id;");
        for (const auto& row : r) {
            crow::json::wvalue product;
            product["id"] = row["id"].as<int>();
            product["name"] = row["name"].as<std::string>();
            product["price"] = format_price(row["price"].as<double>()); // display prices with a fixed number of decimal places
            productsList.push_back(std::move(product));
        }
        // Move the entire vector into a new wvalue
        result["products"] = crow::json::wvalue(std::move(productsList));
    } catch (const std::exception& e) {
        result["error"] = std::string("DB error: ") + e.what();
    }
    return result;
}

// Function to fetch a single product by id.
crow::json::wvalue fetch_product_by_id(int id, bool& found) {
    crow::json::wvalue product;
    found = false;
    try {
        pqxx::connection c(get_db_conn_str());
        pqxx::work txn(c);
        std::stringstream query;
        query << "SELECT id, name, price FROM products WHERE id = " << id << " LIMIT 1;";
        pqxx::result r = txn.exec(query.str());
        if (!r.empty()) {
            found = true;
            product["id"] = r[0]["id"].as<int>();
            product["name"] = r[0]["name"].as<std::string>();
            product["price"] = r[0]["price"].as<double>();
        }
    } catch (const std::exception& e) {
        product["error"] = std::string("DB error: ") + e.what();
    }
    return product;
}

int main()
{
    crow::SimpleApp app;

    // Endpoint to retrieve all products.
    CROW_ROUTE(app, "/products")
    ([](){
        return fetch_products();
    });

    // Endpoint to retrieve a product by id.
    CROW_ROUTE(app, "/products/<int>")
    ([](int id){
        bool found;
        auto product = fetch_product_by_id(id, found);
        if (!found)
            return crow::response(404);
        return crow::response(product);
    });

    app.port(8080).multithreaded().run();
}