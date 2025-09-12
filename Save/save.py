import csv
import os 
import sqlite3 
import json
from pathlib import Path


class Save():
  def __init__(self, db, league, message, file_dir):
    self.db = db
    self.openDB = self.open_db()
    self.con = self.get_con()
    self.cur = self.get_cur()
    self.league = league
    self.message = message
    self.file_dir = file_dir
  
  def db_exists(self):
    db_path = Path(self.db)
    db_uri = f"file:{db_path}?mode=rw"
    try:
        con = sqlite3.connect(db_uri, uri=True, timeout=60)
        cur = con.cursor()
        return con, cur
    except sqlite3.OperationalError:
        print(f"Database '{db_path}' does not exist!")
        return None

  def open_db(self):
    # Connect and insert
    if self.db_exists() is not None:
      con, cur = self.db_exists()
      return con, cur
    
    con = sqlite3.connect(self.db)
    cur = con.cursor()
    return con, cur
  
  def get_con(self):
    try: 
      if self.db:
        con = sqlite3.connect(self.db) 
        return con

    except:
      #print("Error connecting to db!")
      return None 
  
  def get_cur(self):
    try: 
      if self.con:
        cur = self.con.cursor()
        return cur 
    except:
      #print('Error getting cursor!')
      return None
    
  def table_exists(self, con, cur, table_name):
    #con, cur = self.open_db()
    cur.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?;
    """, (table_name,))

    return cur.fetchone() is not None

  def field_exists(self, table, field):
    con, cur = self.open_db()
    cur.execute(f"PRAGMA table_info({table});")
    columns = [row[1] for row in cur.fetchall()]  # row[1] is the column name
    return field in columns 
  
  def scan_ret(self, lst, target):
    for i in range(len(lst)):
      temp = lst[i][0]
      ##print(temp[0] == target)
      if target == temp:
        return True
    return False

  def init_new_db(self):
    # Enable foreign key constraints
    con, cur = self.open_db()
    cur.execute("PRAGMA foreign_keys = ON")
    
    con.commit()
    con.close()
    
    self.init_league()
    self.init_team()
    self.init_player()
    self.init_pitcher()

  def init_league(self):
      con, cur = self.open_db()
      
      # Create league table
      cur.execute(f"""
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

      cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_league_unique
        ON league(leagueID);
    """)

      # set up league cols and fields
      cur.execute("""
      INSERT INTO league (
          leagueID, name, commissioner, treasurer,
          communications, historian, recruitment,
          start, stop
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      """, (
          self.league.leagueID,
          self.league.name,
          self.league.admin['Commissioner'],
          self.league.admin['Historian'],
          self.league.admin['Recruitment'],
          self.league.admin['Communications'],
          self.league.admin['Historian'],
          self.league.admin['Season Start'],
          self.league.admin['Season End']
      ))

      

      # commit created tables and close
      con.commit()
      con.close()
    # call init league
    
  def init_team(self):
      con, cur = self.open_db()

      # Create team table
      cur.execute("""
        CREATE TABLE IF NOT EXISTS team (
            teamID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            leagueID INTEGER NOT NULL,
            league TEXT,
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

      cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_team_unique
        ON team(teamID);
      """)

      con.commit()
      con.close()
    # call init team
    
  def init_player(self):
      con, cur = self.open_db()
      
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
              image TEXT,
              FOREIGN KEY (leagueID) REFERENCES league(leagueID),
              FOREIGN KEY (teamID) REFERENCES team(teamID)
          )
      """)

      cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_player_unique
        ON player(playerID);
      """)
      
      con.commit()
      con.close()
    
  def init_pitcher(self):
      # Create pitcher table
      con, cur = self.open_db()
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
      
      cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_pitcher_unique
        ON pitcher(playerID);
      """)
      
      con.commit()
      con.close()
    
  def save_team(self):
    def keep_attrs(obj):
      keep = ['teamID', 'name', 'leagueID', 'league', 'logo', 'manager', 'players', 'lineup', 'positions', 'wins', 'losses', 'games_played', 'wl_avg', 'bat_avg', 'team_era', 'max_roster']
      dir_list = [x for x in keep if self.sql_safe(x)] 
      ##print(dir_list)
      return dir_list
    
    con, cur = self.open_db()

    if self.table_exists(con, cur, 'team'):
        #print('league exists--table team exists')
        
        objsTeam = self.league.get_all_objs()

        res = cur.execute(f"SELECT teamID FROM team")
        ret = res.fetchall()
        
        # check for league name duplicate 
        if len(ret) == 0:
          #print('no teams in db!')
          for i in range(len(objsTeam)):
            ##print('team to save:', objsTeam[i].name)
            team_name = objsTeam[i].name
            team = objsTeam[i]

            '''if self.scan_ret(ret, team.teamID):
              #print('teamID already exists!')
              continue'''
            
            dir_list = keep_attrs(team) 
            ##print(dir_list)
            cols = []
            vals = []
            ##print(exclude_attrs(team))

            for el in dir_list:
              val = getattr(team, el)
              ##print('val:', val, type(val))
              check_type = [int, str, float, dict, list, type(None)]

              if isinstance(val, (dict)):
                val = json.dumps(val)

              elif isinstance(val, (list)):
                roster = []
                for el in val:
                  ##print(el)
                  player_name = el.name
                  roster.append(player_name)
                
                roster_json = json.dumps(roster)
                ##print(roster_json, type(roster_json))
                val = roster_json
                el = 'players'
              
              elif type(val) not in check_type:
                league_name = val.name 
                val = league_name
              
              cols.append(el)
              vals.append(val)

            placeholders = ", ".join(["?"] * len(vals))
            column_str = ", ".join(cols)

            ##print(placeholders)
            ##print(column_str)
            ##print(vals)
            
            cur.execute(
                  f"INSERT INTO team ({column_str}) VALUES ({placeholders})",
                  tuple(vals)
              )
            
          con.commit()

        # check for league name duplicate 
        elif len(ret) >= 1:
          #print('teams in db!')
          res = cur.execute(f"SELECT teamID FROM team")
          ret = res.fetchall()

          for i in range(len(objsTeam)):
            ##print('team to save:', objsTeam[i].name)
            team = objsTeam[i]
            team_ID = team.teamID
            team_name = team.name

            if self.scan_ret(ret, team_ID):
              #print('teamID already exists!')
              self.update_team(con, cur, team, keep_attrs)
            
            else:
              dir_list = keep_attrs(team)
              ##print(dir_list)
              cols = []
              vals = []
              ##print(exclude_attrs(team))

              for el in dir_list:
                val = getattr(team, el)
                ##print('val:', val, type(val))
                check_type = [int, str, float, dict, list, type(None)]

                if isinstance(val, (dict)):
                  val = json.dumps(val)

                elif isinstance(val, (list)):
                  roster = []
                  for el in val:
                    ##print(el)
                    player_name = el.name
                    roster.append(player_name)
                  
                  roster_json = json.dumps(roster)
                  ##print(roster_json, type(roster_json))
                  val = roster_json
                  el = 'players'
                
                elif type(val) not in check_type:
                  league_name = val.name 
                  val = league_name
                
                cols.append(el)
                vals.append(val)

              placeholders = ", ".join(["?"] * len(vals))
              column_str = ", ".join(cols)

              ##print(placeholders)
              ##print(column_str)
              ##print(vals)
              
              cur.execute(
                    f"INSERT INTO team ({column_str}) VALUES ({placeholders})",
                    tuple(vals)
                )
              
            con.commit()

        con.close()
  
  def update_team(self, con, cur, team_obj, keep_func):
    #print('Update: ', team_obj.name)
    dir_list = keep_func(team_obj)
    team_name = team_obj.name 
    team_ID = team_obj.teamID 
    ##print(team_obj.games_played)

    ##print(dir_list)
    cols = []
    vals = []
    ##print(exclude_attrs(team))

    for el in dir_list:
      val = getattr(team_obj, el)
      ##print('val:', el, val, type(val))
      check_type = [int, str, float, dict, list, type(None)]

      if isinstance(val, (dict)):
        val = json.dumps(val)

      elif isinstance(val, (list)):
        roster = []
        for el in val:
          ##print(el)
          player_name = el.name
          roster.append(player_name)
        
        roster_json = json.dumps(roster)
        ##print(roster_json, type(roster_json))
        val = roster_json
        el = 'players'
      
      elif type(val) not in check_type:
        league_name = val.name 
        val = league_name
      
      cols.append(el)
      vals.append(val)

    #placeholders = ", ".join(["?"] * len(vals))
    #column_str = ", ".join(cols)

    set_clause = ", ".join([f"{col} = ?" for col in cols])
    sql = f"UPDATE team SET {set_clause} WHERE teamID = ?"

    ##print(cols)
    ##print(vals)
    ##print(sql)
    
    # modify command
    cur.execute(sql, vals + [team_ID])
    con.commit()
     
  def save_player(self):
    ##print('save player!')
    def keep_attrs_player(obj):
      keep = ['playerID', 'name', 'leagueID', 'teamID', 'number', 'team', 'positions', 'pa', 'at_bat', 'fielder_choice', 'hit', 'bb', 'hbp', 'so', 'hr', 'rbi', 'runs', 'singles', 'doubles', 'triples', 'sac_fly', 'OBP', 'BABIP', 'SLG', 'AVG', 'ISO', 'image']
      dir_list = [x for x in keep if self.sql_safe(x)] 
      return dir_list
    
    def keep_attrs_pitcher(obj):
      keep = ['name', 'playerID', 'teamID', 'leagueID', 'wins', 'losses', 'era', 'games_played', 'games_completed', 'shutouts', 'save_ops', 'ip', 'p_at_bats', 'p_hits', 'p_runs', 'er', 'p_hb', 'p_so', 'WHIP', 'p_avg', 'k_9', 'bb_9']
      dir_raw = dir(obj)
      dir_list = [x for x in keep if self.sql_safe(x)]
      return dir_list
    
    con, cur = self.open_db()

    if not self.table_exists(con, cur, 'team'):
      #print('team table does not exist!')
      return

    elif not self.table_exists(con, cur, 'player'):
      #print('player table does not exist!')
      return
      
    res = cur.execute("SELECT teamID FROM team")
    ret = [row[0] for row in res.fetchall()]

    # teams exist in the DB/league
    if len(ret) >= 1:
      objsTeam = self.league.get_all_objs()
      ##print(objsTeam)

      for i in range(len(objsTeam)):
        ##print('player team to save:', objsTeam[i])
        team = objsTeam[i]
        team_name = team.name 
        team_ID = team.teamID
        players = team.players

        res = cur.execute("SELECT playerID FROM player")
        ret = [row[0] for row in res.fetchall()]
          
        for player in players: 
          player_name = player.name 
          player_ID = player.playerID
          player_team_ID = player.teamID 
          isPitcher = 'pitcher' in player.positions 
          
          # does player exist in DB ???
          if player_ID in ret:
            #print('match player, wish to update?')

            # is the player a pitcher?
            # if yes, update pitcher and update player tables
            if isPitcher:
              #print('match pitcher, wish to update?')
              self.update_pitcher(con, cur, player, keep_attrs_pitcher)
              self.update_player(con, cur, player, keep_attrs_player) 
              continue

            # if not, update player table only
            self.update_player(con, cur, player, keep_attrs_player)
            continue

          # if playerID not in DB, create new player
          elif player_ID not in ret:
            #print('no match player, wish to create?')

            cols = []
            vals = []

            # if player is a pitcher 
            # exclude players attrs, except name, playerID, teamID, leagueID
            if isPitcher:
              #print('is a pitcher')
              res = cur.execute("SELECT playerID FROM pitcher")
              ret = [row[0] for row in res.fetchall()]

              dir_list = keep_attrs_pitcher(player)
              ##print(dir_list)
          
              for el in dir_list:
                val = getattr(player, el)
                ##print(val, type(val))

                if isinstance(val, (dict, list)):
                  ##print('player val:', el, val, type(val))
                  # represents player positions
                  val = json.dumps(val)

                cols.append(el)
                vals.append(val) 

              placeholders = ", ".join(["?"] * len(vals))
              column_str = ", ".join(cols)

              ##print(placeholders)
              ##print(column_str)
              ##print(cols)
              ##print(vals)
              
              cur.execute(
                    f"INSERT INTO pitcher ({column_str}) VALUES ({placeholders})",
                    tuple(vals)
                )
            
              con.commit()
          
          # reset cols and vals in case of Pitcher isntance
          cols = []
          vals = []

          # regardless of pitcher instance, update all Player attributes
          dir_list = keep_attrs_player(player)
          #print(dir_list)

          for el in dir_list:
            val = getattr(player, el)
            ##print(val, type(val))

            if isinstance(val, (dict, list)):
              ##print('player val:', el, val, type(val))
              # represents player positions
              val = json.dumps(val)
            
            elif el == 'team':

              val = getattr(player, el)
              val = val.name

            cols.append(el)
            vals.append(val) 

          placeholders = ", ".join(["?"] * len(vals))
          column_str = ", ".join(cols)

          #print(placeholders)
          #print(column_str)
          #print(cols)
          #print(vals) 
        
          cur.execute(
                f"INSERT INTO player ({column_str}) VALUES ({placeholders})",
                tuple(vals)
            )
        
          con.commit()

        self.update_team_roster(con, cur, players, team_ID)

    con.close()

  def update_player(self, con, cur, player_obj, keep_func):
    #print('update player:', player_obj.name)
    dir_list = keep_func(player_obj)
    team_name = player_obj.name 
    team_ID = player_obj.teamID
    player_ID = player_obj.playerID
    #print(player_obj.at_bat)

    ##print(dir_list)
    cols = []
    vals = []
    ##print(exclude_attrs(team))

    for el in dir_list:
      val = getattr(player_obj, el)
      ##print('val:', el, val, type(val))
      check_type = [int, str, float, dict, list, type(None)]

      if isinstance(val, (dict)):
        val = json.dumps(val)

      elif isinstance(val, (list)):
        pos = []
        for el in val:
          ##print(el)
          pos.append(el)
        
        pos_json = json.dumps(pos)
        ##print(roster_json, type(roster_json))
        val = pos_json
        el = 'positions'
      
      elif type(val) not in check_type:
        league_name = val.name 
        val = league_name
      
      cols.append(el)
      vals.append(val)

    #placeholders = ", ".join(["?"] * len(vals))
    #column_str = ", ".join(cols)

    set_clause = ", ".join([f"{col} = ?" for col in cols])
    sql = f"UPDATE player SET {set_clause} WHERE playerID = ?"

    #print(cols)
    #print(vals)
    #print(sql)
    
    # modify command
    cur.execute(sql, vals + [player_ID])
    con.commit()

  def update_pitcher(self, con, cur, player_obj, keep_func):
    #print('update player/pitcher:', player_obj.name)
    dir_list = keep_func(player_obj)
    team_name = player_obj.name 
    team_ID = player_obj.teamID
    player_ID = player_obj.playerID
    ##print(team_obj.games_played)

    ##print(dir_list)
    cols = []
    vals = []
    ##print(exclude_attrs(team))

    for el in dir_list:
      val = getattr(player_obj, el)
      ##print('val:', el, val, type(val))
      check_type = [int, str, float, dict, list, type(None)]

      if isinstance(val, (dict)):
        val = json.dumps(val)

      elif isinstance(val, (list)):
        pos = []
        for el in val:
          ##print(el)
          player_name = el.name
          pos.append(player_name)
        
        pos_json = json.dumps(pos)
        ##print(roster_json, type(roster_json))
        val = pos_json
        el = 'positions'
      
      elif type(val) not in check_type:
        league_name = val.name 
        val = league_name
      
      cols.append(el)
      vals.append(val)

    #placeholders = ", ".join(["?"] * len(vals))
    #column_str = ", ".join(cols)

    set_clause = ", ".join([f"{col} = ?" for col in cols])
    sql = f"UPDATE pitcher SET {set_clause} WHERE playerID = ?"

    print(cols)
    print(vals)
    print(sql)
    
    # modify command
    cur.execute(sql, vals + [player_ID])
    con.commit()
     
  def update_team_roster(self, con, cur, roster, teamID):
    res = cur.execute("SELECT teamID FROM team")
    ret = res.fetchall()
    roster_JSON = json.dumps([x.name for x in roster])
    team_ids = [row[0] for row in ret]

    ##print(ret)
    if len(ret) == 0:
      #print('No teams in league!')
      return
    
    if teamID in team_ids:
      #print('match: ', teamID)
      
      cur.execute(
          """UPDATE team 
          SET players = ? 
          WHERE teamID = ?
          """, 
          (roster_JSON, teamID)
        )
      
      con.commit()
      
  def sql_safe(self, val):
    return isinstance(val, (type(None), int, float, str))

  def save_csv(self, file_name="league_db"):
    con, cur = self.open_db()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    
    # Ensure the directory exists
    os.makedirs("/home/Stat_Man_Pro", exist_ok=True)

    for table in tables:
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

        column_names = [description[0] for description in cur.description]

        file_name = f"{file_name}{table}.csv"
        file_path = os.path.join("/home/Stat_Man_Pro", file_name)

        with open(file_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
            writer.writerows(rows)

    con.close()

  def save_master(self):
    con, cur = self.open_db()

    res = cur.execute("SELECT name from sqlite_master where type='table'")
    ret = [row[0] for row in res.fetchall()]

    if len(ret) == 0:
      print('no tables exist - init league')
      self.init_new_db()
    
    print('update team/player/pitcher fields')
    self.save_team()
    self.save_player()

    self.save_csv()

    con.commit()
    con.close()

