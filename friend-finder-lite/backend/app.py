from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv
import os
from collections import defaultdict

load_dotenv()

app = Flask(__name__)
CORS(app)

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    try:
        city = request.args.get('city')
        neighborhood = request.args.get('neighborhood')
        interest = request.args.get('interest')
        activity = request.args.get('activity')
        availability = request.args.get('availability')

        query = supabase.table('profiles').select('*, interests(tag), activities(activity)')

        if city:
            query = query.eq('city', city)
        if neighborhood:
            query = query.eq('neighborhood', neighborhood)
        if availability:
            query = query.contains('availability', [availability])

        result = query.execute()
        profiles = result.data

        if interest:
            profiles = [p for p in profiles if any(i['tag'] == interest for i in p.get('interests', []))]

        if activity:
            profiles = [p for p in profiles if any(a['activity'] == activity for a in p.get('activities', []))]

        return jsonify(profiles), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profiles/<profile_id>', methods=['GET'])
def get_profile(profile_id):
    try:
        result = supabase.table('profiles').select('*, interests(tag), activities(activity)').eq('id', profile_id).execute()

        if not result.data or len(result.data) == 0:
            return jsonify({'error': 'Profile not found'}), 404

        return jsonify(result.data[0]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    try:
        data = request.json

        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400

        profile_data = {
            'name': data['name'],
            'bio': data.get('bio', ''),
            'city': data.get('city', ''),
            'neighborhood': data.get('neighborhood', ''),
            'availability': data.get('availability', [])
        }

        result = supabase.table('profiles').insert(profile_data).execute()
        profile = result.data[0]
        profile_id = profile['id']

        if data.get('interests'):
            interests_data = [{'profile_id': profile_id, 'tag': tag} for tag in data['interests']]
            supabase.table('interests').insert(interests_data).execute()

        if data.get('activities'):
            activities_data = [{'profile_id': profile_id, 'activity': act} for act in data['activities']]
            supabase.table('activities').insert(activities_data).execute()

        return jsonify(profile), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profiles/<profile_id>', methods=['PUT'])
def update_profile(profile_id):
    try:
        data = request.json

        profile_data = {}
        if 'name' in data:
            profile_data['name'] = data['name']
        if 'bio' in data:
            profile_data['bio'] = data['bio']
        if 'city' in data:
            profile_data['city'] = data['city']
        if 'neighborhood' in data:
            profile_data['neighborhood'] = data['neighborhood']
        if 'availability' in data:
            profile_data['availability'] = data['availability']

        profile_data['updated_at'] = 'now()'

        result = supabase.table('profiles').update(profile_data).eq('id', profile_id).execute()

        if 'interests' in data:
            supabase.table('interests').delete().eq('profile_id', profile_id).execute()
            if data['interests']:
                interests_data = [{'profile_id': profile_id, 'tag': tag} for tag in data['interests']]
                supabase.table('interests').insert(interests_data).execute()

        if 'activities' in data:
            supabase.table('activities').delete().eq('profile_id', profile_id).execute()
            if data['activities']:
                activities_data = [{'profile_id': profile_id, 'activity': act} for act in data['activities']]
                supabase.table('activities').insert(activities_data).execute()

        return jsonify(result.data[0]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profiles/<profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    try:
        supabase.table('profiles').delete().eq('id', profile_id).execute()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profiles/<profile_id>/matches', methods=['GET'])
def get_matches(profile_id):
    try:
        profile_result = supabase.table('profiles').select('*, interests(tag), activities(activity)').eq('id', profile_id).execute()

        if not profile_result.data or len(profile_result.data) == 0:
            return jsonify({'error': 'Profile not found'}), 404

        current_profile = profile_result.data[0]
        current_interests = set([i['tag'] for i in current_profile.get('interests', [])])
        current_activities = set([a['activity'] for a in current_profile.get('activities', [])])

        all_profiles = supabase.table('profiles').select('*, interests(tag), activities(activity)').neq('id', profile_id).execute()

        matches = []
        for profile in all_profiles.data:
            profile_interests = set([i['tag'] for i in profile.get('interests', [])])
            profile_activities = set([a['activity'] for a in profile.get('activities', [])])

            shared_interests = current_interests.intersection(profile_interests)
            shared_activities = current_activities.intersection(profile_activities)

            match_score = len(shared_interests) + len(shared_activities)

            if match_score > 0:
                matches.append({
                    **profile,
                    'match_score': match_score,
                    'shared_interests': list(shared_interests),
                    'shared_activities': list(shared_activities)
                })

        matches.sort(key=lambda x: x['match_score'], reverse=True)

        return jsonify(matches), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/connections', methods=['POST'])
def create_connection():
    try:
        data = request.json

        if not data.get('sender_id') or not data.get('receiver_id'):
            return jsonify({'error': 'sender_id and receiver_id are required'}), 400

        connection_data = {
            'sender_id': data['sender_id'],
            'receiver_id': data['receiver_id'],
            'status': 'pending'
        }

        result = supabase.table('connections').insert(connection_data).execute()
        return jsonify(result.data[0]), 201
    except Exception as e:
        if 'duplicate key' in str(e).lower():
            return jsonify({'error': 'Connection request already exists'}), 400
        return jsonify({'error': str(e)}), 500

@app.route('/api/connections/<connection_id>', methods=['PUT'])
def update_connection(connection_id):
    try:
        data = request.json

        if 'status' not in data or data['status'] not in ['accepted', 'declined']:
            return jsonify({'error': 'Valid status required (accepted or declined)'}), 400

        update_data = {
            'status': data['status'],
            'updated_at': 'now()'
        }

        result = supabase.table('connections').update(update_data).eq('id', connection_id).execute()
        return jsonify(result.data[0]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/connections/sent/<profile_id>', methods=['GET'])
def get_sent_connections(profile_id):
    try:
        result = supabase.table('connections').select('*, receiver:profiles!connections_receiver_id_fkey(*)').eq('sender_id', profile_id).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/connections/received/<profile_id>', methods=['GET'])
def get_received_connections(profile_id):
    try:
        result = supabase.table('connections').select('*, sender:profiles!connections_sender_id_fkey(*)').eq('receiver_id', profile_id).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/connections/friends/<profile_id>', methods=['GET'])
def get_friends(profile_id):
    try:
        sent_result = supabase.table('connections').select('*, receiver:profiles!connections_receiver_id_fkey(*)').eq('sender_id', profile_id).eq('status', 'accepted').execute()

        received_result = supabase.table('connections').select('*, sender:profiles!connections_sender_id_fkey(*)').eq('receiver_id', profile_id).eq('status', 'accepted').execute()

        friends = []
        for conn in sent_result.data:
            friends.append(conn['receiver'])
        for conn in received_result.data:
            friends.append(conn['sender'])

        return jsonify(friends), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
