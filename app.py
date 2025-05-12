from flask import Flask, request, jsonify, render_template
from models import db, Simulation
import random
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simulations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

def run_simulation(target_count, scroll_cost, success_rate, max_attempts):
    dist = {}
    total_scrolls = total_cost = 0

    for _ in range(target_count):
        succ = 0; used = 0
        for _ in range(max_attempts):
            used += 1
            if random.random() < success_rate:
                succ += 1
            else:
                break
        dist[succ] = dist.get(succ, 0) + 1
        total_scrolls += used
        total_cost += used * scroll_cost

    return dist, total_scrolls, total_cost

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', lastResult=None)


# API：模擬一次，並存 DB
@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    data = request.json
    tc = int(data['target_count'])
    sc = int(data['scroll_cost'])
    sr = float(data['success_rate'])
    ma = int(data['max_attempts'])

    dist, tot_s, tot_c = run_simulation(tc, sc, sr, ma)

    sim = Simulation(
        target_count=tc, scroll_cost=sc,
        success_rate=sr, max_attempts=ma,
        total_scrolls=tot_s, total_cost=tot_c,
        distribution=json.dumps(dist)
    )
    db.session.add(sim)
    db.session.commit()

    return jsonify({
        'id': sim.id,
        'timestamp': sim.timestamp.isoformat(),
        'target_count': tc,
        'scroll_cost': sc,
        'success_rate': sr,
        'max_attempts': ma,
        'total_scrolls': tot_s,
        'total_cost': tot_c,
        'distribution': dist
    })

# API：取所有歷史紀錄
@app.route('/api/records')
def api_records():
    sims = Simulation.query.order_by(Simulation.id.desc()).all()
    out = []
    for s in sims:
        out.append({
            'id': s.id,
            'timestamp': s.timestamp.isoformat(),
            'target_count': s.target_count,
            'scroll_cost': s.scroll_cost,
            'success_rate': s.success_rate,
            'max_attempts': s.max_attempts,
            'total_scrolls': s.total_scrolls,
            'total_cost': s.total_cost,
            'distribution': json.loads(s.distribution)
        })
    return jsonify(out)

@app.route('/records')
def records_page():
    return render_template('records.html')


if __name__ == '__main__':
    app.run(debug=True)
