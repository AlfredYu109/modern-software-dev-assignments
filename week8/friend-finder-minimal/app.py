import os
import sqlite3

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

DATABASE = "friend_finder.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT,
            city TEXT,
            interests TEXT,
            activities TEXT,
            availability TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES profiles (id),
            FOREIGN KEY (receiver_id) REFERENCES profiles (id),
            UNIQUE(sender_id, receiver_id)
        )
    """
    )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/profiles", methods=["GET"])
def get_profiles():
    conn = get_db()
    cursor = conn.cursor()

    interest = request.args.get("interest")
    city = request.args.get("city")
    availability = request.args.get("availability")

    query = "SELECT * FROM profiles"
    conditions = []
    params = []

    if interest:
        conditions.append("interests LIKE ?")
        params.append(f"%{interest}%")
    if city:
        conditions.append("city LIKE ?")
        params.append(f"%{city}%")
    if availability:
        conditions.append("availability LIKE ?")
        params.append(f"%{availability}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    profiles = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in profiles])


@app.route("/api/profiles/<int:profile_id>", methods=["GET"])
def get_profile(profile_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
    profile = cursor.fetchone()
    conn.close()

    if profile is None:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify(dict(profile))


@app.route("/api/profiles", methods=["POST"])
def create_profile():
    data = request.json

    if not data.get("name"):
        return jsonify({"error": "Name is required"}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO profiles (name, bio, city, interests, activities, availability)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            data.get("name"),
            data.get("bio", ""),
            data.get("city", ""),
            (
                ",".join(data.get("interests", []))
                if isinstance(data.get("interests"), list)
                else data.get("interests", "")
            ),
            (
                ",".join(data.get("activities", []))
                if isinstance(data.get("activities"), list)
                else data.get("activities", "")
            ),
            data.get("availability", ""),
        ),
    )

    conn.commit()
    profile_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": profile_id, "message": "Profile created successfully"}), 201


@app.route("/api/profiles/<int:profile_id>", methods=["PUT"])
def update_profile(profile_id):
    data = request.json

    if not data.get("name"):
        return jsonify({"error": "Name is required"}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE profiles
        SET name = ?, bio = ?, city = ?, interests = ?, activities = ?, availability = ?
        WHERE id = ?
    """,
        (
            data.get("name"),
            data.get("bio", ""),
            data.get("city", ""),
            (
                ",".join(data.get("interests", []))
                if isinstance(data.get("interests"), list)
                else data.get("interests", "")
            ),
            (
                ",".join(data.get("activities", []))
                if isinstance(data.get("activities"), list)
                else data.get("activities", "")
            ),
            data.get("availability", ""),
            profile_id,
        ),
    )

    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    if rows_affected == 0:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify({"message": "Profile updated successfully"})


@app.route("/api/profiles/<int:profile_id>", methods=["DELETE"])
def delete_profile(profile_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM connections WHERE sender_id = ? OR receiver_id = ?", (profile_id, profile_id)
    )
    cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))

    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    if rows_affected == 0:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify({"message": "Profile deleted successfully"})


@app.route("/api/matches/<int:profile_id>", methods=["GET"])
def get_matches(profile_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
    user_profile = cursor.fetchone()

    if user_profile is None:
        conn.close()
        return jsonify({"error": "Profile not found"}), 404

    user_interests = (
        set(filter(None, user_profile["interests"].split(",")))
        if user_profile["interests"]
        else set()
    )
    user_activities = (
        set(filter(None, user_profile["activities"].split(",")))
        if user_profile["activities"]
        else set()
    )

    cursor.execute("SELECT * FROM profiles WHERE id != ?", (profile_id,))
    all_profiles = cursor.fetchall()
    conn.close()

    matches = []
    for profile in all_profiles:
        profile_interests = (
            set(filter(None, profile["interests"].split(","))) if profile["interests"] else set()
        )
        profile_activities = (
            set(filter(None, profile["activities"].split(","))) if profile["activities"] else set()
        )

        shared_interests = user_interests & profile_interests
        shared_activities = user_activities & profile_activities
        match_score = len(shared_interests) + len(shared_activities)

        if match_score > 0:
            profile_dict = dict(profile)
            profile_dict["match_score"] = match_score
            profile_dict["shared_interests"] = list(shared_interests)
            profile_dict["shared_activities"] = list(shared_activities)
            matches.append(profile_dict)

    matches.sort(key=lambda x: x["match_score"], reverse=True)

    return jsonify(matches)


@app.route("/api/connections", methods=["POST"])
def send_connection_request():
    data = request.json

    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")

    if not sender_id or not receiver_id:
        return jsonify({"error": "sender_id and receiver_id are required"}), 400

    if sender_id == receiver_id:
        return jsonify({"error": "Cannot send connection to yourself"}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM connections
        WHERE sender_id = ? AND receiver_id = ?
    """,
        (sender_id, receiver_id),
    )

    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Connection request already exists"}), 400

    cursor.execute(
        """
        INSERT INTO connections (sender_id, receiver_id, status)
        VALUES (?, ?, 'pending')
    """,
        (sender_id, receiver_id),
    )

    conn.commit()
    connection_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": connection_id, "message": "Connection request sent successfully"}), 201


@app.route("/api/connections/<int:profile_id>/incoming", methods=["GET"])
def get_incoming_connections(profile_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.*, p.name, p.bio, p.interests, p.activities
        FROM connections c
        JOIN profiles p ON c.sender_id = p.id
        WHERE c.receiver_id = ? AND c.status = 'pending'
    """,
        (profile_id,),
    )

    connections = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in connections])


@app.route("/api/connections/<int:profile_id>/friends", methods=["GET"])
def get_friends(profile_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT p.* FROM profiles p
        JOIN connections c ON (p.id = c.sender_id OR p.id = c.receiver_id)
        WHERE (c.sender_id = ? OR c.receiver_id = ?)
        AND c.status = 'accepted'
        AND p.id != ?
    """,
        (profile_id, profile_id, profile_id),
    )

    friends = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in friends])


@app.route("/api/connections/<int:connection_id>/accept", methods=["PUT"])
def accept_connection(connection_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE connections
        SET status = 'accepted'
        WHERE id = ?
    """,
        (connection_id,),
    )

    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    if rows_affected == 0:
        return jsonify({"error": "Connection not found"}), 404

    return jsonify({"message": "Connection accepted"})


@app.route("/api/connections/<int:connection_id>/decline", methods=["PUT"])
def decline_connection(connection_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE connections
        SET status = 'declined'
        WHERE id = ?
    """,
        (connection_id,),
    )

    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    if rows_affected == 0:
        return jsonify({"error": "Connection not found"}), 404

    return jsonify({"message": "Connection declined"})


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
        print(f"Database {DATABASE} initialized")
    app.run(debug=True, port=5000, host="0.0.0.0")
