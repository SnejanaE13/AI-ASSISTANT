import uvicorn
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FastAPI application.")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database.")
    args = parser.parse_args()

    if args.init_db:
        from app.db.init_db import init_db
        init_db()
        print("Database initialized.")
    else:
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
