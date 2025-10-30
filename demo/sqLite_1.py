import sqlite3 
import json
import os

# init db with general name 
  # con = sqlite3.connect('stat_mg.db')
  # cur = con.cursor()


# set up league table, leagueID 
  # league ID generator
  # cur.execute("CREATE TABLE league(name, leagueID, commissioner, treasurer, communications, historian, recruitment, start, stop)") 
  # con.commit()


# set up team table, leagueID, teamID 
  # team ID generator 
  # cur.execute("CREATE TABLE team(name, leagueID, teamID, logo, manager, players(list), lineup (dict), positions(dict), wins, losses, games_played, wl_avg, bat_avg, team_era, max_roster)") 
  # con.commit()


# set up player table, leagueID, teamID and playerID
  # player ID generator
  # cur.execute("CREATE TABLE player(name, leagueID, teamID, playerID, number, team, positions(list), pa, at_bat, fielder_choice, hit, bb, hbp, so, hr, rbi, runs, singles, doubles, triples, sac_fly, OBP, BABIP, SLG, AVG, ISO, max(None), image)") 
  # con.commit()


# set up pitcher table, leagueID, teamID, playerID
  # player ID (shared with player table) 
  # cur.execute("CREATE TABLE player(name, leagueID, teamID, playerID, wins, losses, era, games_played, games_started, games_completed, shutouts, saves, save_ops, ip, p_at_bats, p_hits, p_runs, er, p_hr, p_hb, p_bb, p_so, WHIP, p_AVG, k_9, bb_9)") 
  # con.commit()

class Player():
  def __init__(self, name, number, team, message, positions=[], parent=None):
    self.name = name 
    self.number = number 
    self.team = team
    self.positions = positions
    self.pa = 0
    self.at_bat = 0 
    self.fielder_choice = 0
    self.hit = 0 
    self.bb = 0
    self.hbp = 0
    self.so = 0
    self.hr = 0
    self.rbi = 0
    self.runs = 0
    self.singles = 0
    self.doubles = 0
    self.triples = 0
    self.sac_fly = 0
    self.OBP = 0
    self.BABIP = 0
    self.SLG = 0
    self.AVG = 0
    self.ISO = 0
    self.max = 0
    self.image = None

class Pitcher(Player):
  def __init__(self, name, number, team, message, positions=[]):
    super().__init__(name, number, team, message, positions=[])
  
    # player pitcher gen attr
    self.name = name 
    self.number = number 
    self.team = team
    self.positions = positions
    self.image = None
    self.message = message

    # pitching attr
    self.wins = 0 
    self.losses = 0 
    self.era = 0 
    self.games_played = 0 

    # to incorporate ...
    self.games_started = 0 
    self.games_completed = 0 
    self.shutouts = 0 
    self.saves = 0 
    self.save_ops = 0
    self.ip = 0 
    self.p_at_bats = 0
    self.p_hits = 0 
    self.p_runs = 0
    self.er = 0 
    self.p_hr = 0 
    self.p_hb = 0 
    self.p_bb = 0 
    self.p_so = 0 
    self.WHIP = 0 
    self.p_avg = 0 
    self.k_9 = 0 
    self.bb_9 = 0 

pos_1 = ['left field', 'right field']
pos_2 = ['second base', 'short stop', 'pitcher']

player_1 = Player('Name', 18, 'team', None, pos_1)
player_2 = Pitcher('Name', 18, 'team', None, pos_2)

# init db with all necessary tables 
con = sqlite3.connect('stat_mg.db')
cur = con.cursor()
db = 'stat_mg.db'

def init_db():
    # Enable foreign key constraints
    cur.execute("PRAGMA foreign_keys = ON")

    # Create league table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS league (
            leagueID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            commissioner TEXT,
            treasurer TEXT,
            communications TEXT,
            historian TEXT,
            recruitment TEXT,
            start TEXT,
            stop TEXT
        )
    """)

    # Create team table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS team (
            teamID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            leagueID INTEGER NOT NULL,
            logo TEXT,
            manager TEXT,
            players TEXT,         -- JSON stringified list
            lineup TEXT,          -- JSON stringified dict
            positions TEXT,       -- JSON stringified dict
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            wl_avg REAL DEFAULT 0.0,
            bat_avg REAL DEFAULT 0.0,
            team_era REAL DEFAULT 0.0,
            max_roster INTEGER,
            FOREIGN KEY (leagueID) REFERENCES league(leagueID)
        )
    """)

    # Create player table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS player (
            playerID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            leagueID INTEGER NOT NULL,
            teamID INTEGER NOT NULL,
            number INTEGER,
            team TEXT,
            positions TEXT,       -- JSON stringified list
            pa INTEGER DEFAULT 0,
            at_bat INTEGER DEFAULT 0,
            fielder_choice INTEGER DEFAULT 0,
            hit INTEGER DEFAULT 0,
            bb INTEGER DEFAULT 0,
            hbp INTEGER DEFAULT 0,
            so INTEGER DEFAULT 0,
            hr INTEGER DEFAULT 0,
            rbi INTEGER DEFAULT 0,
            runs INTEGER DEFAULT 0,
            singles INTEGER DEFAULT 0,
            doubles INTEGER DEFAULT 0,
            triples INTEGER DEFAULT 0,
            sac_fly INTEGER DEFAULT 0,
            OBP REAL DEFAULT 0.0,
            BABIP REAL DEFAULT 0.0,
            SLG REAL DEFAULT 0.0,
            AVG REAL DEFAULT 0.0,
            ISO REAL DEFAULT 0.0,
            max_stat REAL,
            image TEXT,
            FOREIGN KEY (leagueID) REFERENCES league(leagueID),
            FOREIGN KEY (teamID) REFERENCES team(teamID)
        )
    """)

    # Create pitcher table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pitcher (
            playerID INTEGER PRIMARY KEY,
            leagueID INTEGER NOT NULL,
            teamID INTEGER NOT NULL,
            name TEXT NOT NULL,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            era REAL DEFAULT 0.0,
            games_played INTEGER DEFAULT 0,
            games_started INTEGER DEFAULT 0,
            games_completed INTEGER DEFAULT 0,
            shutouts INTEGER DEFAULT 0,
            saves INTEGER DEFAULT 0,
            save_ops INTEGER DEFAULT 0,
            ip REAL DEFAULT 0.0,
            p_at_bats INTEGER DEFAULT 0,
            p_hits INTEGER DEFAULT 0,
            p_runs INTEGER DEFAULT 0,
            er INTEGER DEFAULT 0,
            p_hr INTEGER DEFAULT 0,
            p_hb INTEGER DEFAULT 0,
            p_bb INTEGER DEFAULT 0,
            p_so INTEGER DEFAULT 0,
            WHIP REAL DEFAULT 0.0,
            p_AVG REAL DEFAULT 0.0,
            k_9 REAL DEFAULT 0.0,
            bb_9 REAL DEFAULT 0.0,
            FOREIGN KEY (playerID) REFERENCES player(playerID),
            FOREIGN KEY (leagueID) REFERENCES league(leagueID),
            FOREIGN KEY (teamID) REFERENCES team(teamID)
        )
    """)
    con.commit()
    con.close()
  

def get_val():
  res = cur.execute("SELECT name FROM sqlite_master")
  ret = res.fetchone()
  return ret


class Create():
  def __init__(self, objPlayer, objPTeam, type, db, con, cur, leagueID=None, teamID=None, playerID=None):
    self.objP = objPlayer 
    self.objT = objPTeam
    self.leagueID = leagueID 
    self.teamID = teamID
    self.playerID = playerID
    self.objP_type = type
    self.file_path = getattr(self.objP, 'image')
    self.db = db
    self.con = con 
    self.cur = cur

  
  def __str__(self):
    dir_lst = [x for x in dir(self) if "_" not in x]
    ret = ''
    for el in dir_lst:
      #print(el)
      ret += f'attr: {el} : {getattr(self, el)}\n'
    return ret
  

  def gen_variables(self):
    dir_lst = self.get_dir()
    for el in dir_lst:
      stat = list(el.keys())[0]
      val = list(el.values())[0]
      #print(stat, val)
      setattr(self, stat, val)


  def get_dir(self):
    dir_objP = dir(self.objP)
    dir_lst = [{x:getattr(self.objP, x)} for x in dir_objP if "_" not in x] 
    return dir_lst


  def create_player(self):
    # Validate logo path
    try :
      if not os.path.isfile(self.file_path):
          raise FileNotFoundError(f"Image file not found: {self.file_path}")
    except:
      print('Error updating player image!')

    
    # Connect and insert
    con = sqlite3.connect('stat_mg.db')
    cur = con.cursor()

    pos = getattr(self.objP, 'positions')
    # Serialize complex fields
    pos_json = json.dumps(getattr(self.objP, 'positions'))


    # search players, team_era, bat_avg fields in team TABLE according to teamID
    cur.execute("SELECT players, team_era, bat_avg FROM team WHERE team_id = ?", (self.teamID,))
    row = cur.fetchone()
    if not row:
        print(f"Team {self.teamID} not found.")
        return
    
    players_json, team_era, bat_avg = row
    current_players = json.loads(players_json) if players_json else []

    for el in current_players:
      tempPlayerID = el.get("playerID")
      if tempPlayerID == self.playerID:
         
        # update player level stats 
        cur.execute("""
        UPDATE player
        SET pa=?, at_bat=?, fielder_choice=?, hit=?,
            bb=?, hbp=?, so=?, hr=?, rbi=?, 
            runs=?, singles=?, doubles=?, triples=?, sac_fly=?,
            OBP=?, BABIP=?, SLG=?, AVG=?, ISO=?
        WHERE playerID = ?
        """, (getattr(self.objP, 'pa'), getattr(self.objP, 'at_bat'), getattr(self.objP, 'fielder_choice'), getattr(self.objP, 'hit'),
              getattr(self.objP, 'bb'), getattr(self.objP, 'hbp'), getattr(self.objP, 'so'),  getattr(self.objP, 'hr'),  getattr(self.objP, 'rbi'),
              getattr(self.objP, 'runs'), getattr(self.objP, 'singles'), getattr(self.objP, 'doubles'), getattr(self.objP, 'triples'),
              getattr(self.objP, 'sac_fly'), getattr(self.objP, 'OBP'), getattr(self.objP, 'BABIP'), getattr(self.objP, 'SLG'), getattr(self.objP, 'AVG'),
              getattr(self.objP, 'ISO'), self.playerID))
        con.commit()

        # update team level stats
        cur.execute("""
        UPDATE team
        SET bat_avg=?, team_era=?
        WHERE teamID = ?
        """, (getattr(self.objT, 'bat_avg'), getattr(self.objT, 'team_era'), self.teamID))
        con.commit()

        return 
    
    # if player id not found in team current players 
    # create new player
    # add new payer to team current players
    # update team level stats
    



    
    # 25 columns
    cur.execute("""
        INSERT INTO player (
            name, leagueID, teamID, playerID, team, 
            positions, pa, at_bat, fielder_choice, hit,
            bb, hbp, so, hr, rbi, 
            runs, singles, doubles, triples, sac_fly,
            OBP, BABIP, SLG, AVG, ISO
            
        ) VALUES (?, ?, ?, ?, ?, 
                  ?, ?, ?, ?, ?, 
                  ?, ?, ?, ?, ?, 
                  ?, ?, ?, ?, ?, 
                  ?, ?, ?, ?, ?)
    """, (
        getattr(self.objP, 'name'), self.leagueID, self.teamID, self.playerID, getattr(self.objP, 'team'), 
        pos_json, getattr(self.objP ,'pa'), getattr(self.objP, 'at_bat'), getattr(self.objP, 'fielder_choice'), getattr(self.objP, 'hit'),
        getattr(self.objP, 'bb'), getattr(self.objP, 'hbp'), getattr(self.objP, 'so'), getattr(self.objP, 'hr'), getattr(self.objP, 'rbi'),
        getattr(self.objP, 'runs'), getattr(self.objP, 'singles'), getattr(self.objP, 'doubles'), getattr(self.objP, 'triples'), getattr(self.objP, 'sac_fly'),
        getattr(self.objP, 'OBP'), getattr(self.objP, 'BABIP'), getattr(self.objP, 'SLG'), getattr(self.objP, 'AVG'), getattr(self.objP, 'ISO')
    ))

    player_id = cur.lastrowid
    con.commit()

    if 'pitcher' in pos:
      cur.execute("""
            INSERT INTO pitcher (
                name, leagueID, teamID, playerID, wins, 
                losses, games_played, era, games_started, games_completed, 
                shutouts, saves, save_ops, ip, p_at_bats, 
                p_hits, p_runs, er, p_hr, p_hb, 
                p_bb, p_so, WHIP, p_avg, k_9, 
                bb_9
            ) VALUES (?, ?, ?, ?, ?, 
                      ?, ?, ?, ?, ?, 
                      ?, ?, ?, ?, ?, 
                      ?, ?, ?, ?, ?, 
                      ?, ?, ?, ?, ?,
                      ?
                      )
        """, (
            getattr(self.objP, 'name'), self.leagueID, self.teamID, self.playerID, getattr(self.objP, 'wins'), 
            getattr(self.objP ,'losses'), getattr(self.objP, 'games_played'), getattr(self.objP, 'era'), getattr(self.objP, 'games_started'), getattr(self.objP, 'games_completed'),
            getattr(self.objP, 'shutouts'), getattr(self.objP, 'saves'), getattr(self.objP, 'save_ops'), getattr(self.objP, 'ip'), getattr(self.objP, 'p_at_bats'), 
            getattr(self.objP, 'p_hits'), getattr(self.objP, 'p_runs'), getattr(self.objP, 'er'), getattr(self.objP, 'p_hr'), getattr(self.objP, 'p_hb'), 
            getattr(self.objP, 'p_bb'), getattr(self.objP, 'p_so'), getattr(self.objP, 'WHIP'), getattr(self.objP, 'p_avg'), getattr(self.objP, 'k_9'),
            getattr(self.objP, 'bb_9')
        )) 

      player_id = cur.lastrowid
      con.commit()
      con.close()

    return player_id

    

# db initialized 
# league table
# team table 
# player table
init_db()

create_1 = Create(player_1, 'player',  db, con, cur, leagueID=1, teamID=2, playerID=3)
#create_1.create_player()

create_2 = Create(player_2, 'player', db, con, cur, leagueID=1, teamID=2, playerID=4)
create_2.create_player()

#create_1.gen_variables()
#create_2.gen_variables()
#print(create)


