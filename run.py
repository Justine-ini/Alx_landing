# Importing the Flask app instance from the quikvote package
from quikvote import app

# This conditional block ensures that the app is only run if this script is executed directly,
# not when it's imported as a module in another script.
if __name__ == "__main__":
    # Running the Flask app on the specified host (0.0.0.0) and enabling debug mode for development
    app.run(host="0.0.0.0", debug=True)
