# run.py

# This is the main entry point for the GradebookCalc application.
# To start the application, execute this script from your terminal:
# python run.py

from gradebook_calc import create_app
import os

config_name = os.environ.get('FLASK_CONFIG') or 'default'
# Create the Flask application instance using the app factory pattern.
# This pattern is useful for configurations, testing, and multiple instances.
app = create_app(config_name)

if __name__ == '__main__':
    # The __name__ == '__main__' block ensures that the server is only run
    # when the script is executed directly (and not when imported).

    # Get port from environment variable or default to 5001
    port = int(os.environ.get("PORT", 5001))
    
    # app.run() starts the Flask's built-in development web server.
    #
    # - host='0.0.0.0' makes the server accessible from any network interface,
    #   not just localhost. This is useful for testing on other devices
    #   on the same network.
    # - port=port sets the port the server will listen on.
    # - debug=True enables the Flask debugger. This provides detailed error
    #   pages and automatically reloads the server when you make code changes.
    #   IMPORTANT: Never run with debug=True in a production environment!
    print(f"Starting GradebookCalc server in '{config_name}' mode...")
    print(f"Starting GradebookCalc server at http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)


