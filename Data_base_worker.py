import pandas
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, exc, orm, engine, ForeignKey, \
    Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session
import os
import time
import random

Base = declarative_base()

Link_len = 255
Name_len = 255
Type_len = 255
Activity_string_len = 255
City_name_len = 255
Country_name_len = 255
Description_len = 255
Date_string_len = 255
Status_len = 255
Post_len = 500
Vec_column_len = 1000
metadata = MetaData
my_path = __file__[:__file__.rfind('\\') + 1]
database_path = my_path + 'test.db'
database_full_name = 'sqlite:///' + database_path
"""
Groups_table = Table('Groups', metadata,
                     Column('group_id', Integer, primary_key=True),
                     Column('vk_id', Integer),
                     Column("link", String(Link_len)),
                     Column("name", String(Name_len)),
                     Column("screen_name", String(Name_len)),
                     Column("is_closed", Boolean),
                     Column("deactivated", Boolean),
                     Column("group_type", String(Type_len)),
                     Column("has_photo", Boolean),
                     Column("photo_50", String(Link_len)),
                     Column("photo_100", String(Link_len)),
                     Column("photo_200", String(Link_len)),
                     Column("activity", String(Activity_string_len)),
                     Column("age_limits", Integer),
                     Column("city", String(City_name_len)),
                     Column("country", String(Country_name_len)),
                     Column("description", String(Description_len)),
                     Column("members_count", Integer),
                     Column("public_date_label", String(Date_string_len)),
                     Column("site", String(Link_len)),
                     Column("status", String(Status_len)),
                     Column("verified", Boolean),
                     Column("wiki_page", String(Link_len)),
                     Column("update_posts_time", String(Date_string_len)),
                     Column("update_vec_time", String(Date_string_len))
                     )

Posts_table = Table("Posts", metadata,
                    Column('vec_id', Integer, primary_key=True),
                    "..."
                    )
Vecs_story_table = Table("Vec_story", metadata,
                         Column('id', Integer, primary_key=True),
                         Column('group', Integer, ForeignKey('Groups.group_id')),
                         Column("Date_of_info", String(Date_string_len), ForeignKey('Groups.update_posts_time')),
                         Column("n1", BOOLEAN),
                         Column("n1", BOOLEAN),
                         )
"""


def check_database():
    with sqlalchemy.create_engine(database_full_name).connect() as connection:
        if not os.path.exists("test.db"):
            create_database(connection)
            Base.metadata.create_all(bind=engine)
            connection.execute("commit")


def create_database(connection):
    connection.execute('CREATE DATABASE my_database')
    connection.execute("commit")


class DB_worker():
    def __init__(self):
        check_database()
        self.my_engine = sqlalchemy.create_engine(database_full_name, convert_unicode=True)
        self.session = Session(bind=self.my_engine)
        Base.metadata.create_all(bind=self.my_engine)

    def write_group_to_base(self, group_data, group_posts):
        new_group = Groups()
        # new_group.base_id = random.randint(0, 9999)
        new_group.vk_id = group_data['id']
        new_group.link = "vk.com/" + str(group_data['id'])
        new_group.name = group_data['name']
        if 'screen_name' in group_data and group_data['screen_name']:
            new_group.screen_name = group_data['screen_name']
        else:
            new_group.screen_name = '--'
        if 'is_closed' in group_data:
            new_group.is_closed = bool(group_data['is_closed'])
        else:
            new_group.is_closed = False
        if 'deactivated' in group_data:
            new_group.deactivated = bool(group_data['deactivated'])
        else:
            new_group.deactivated = False
        if 'type' in group_data:
            new_group.group_type = group_data['type']
        else:
            new_group.group_type = "--"
        new_group.photo_50 = group_data['photo_50']
        new_group.photo_100 = group_data['photo_100']
        new_group.photo_200 = group_data['photo_200']
        if 'activity' in group_data:
            new_group.activity = group_data['activity']
        else:
            new_group.activity = '--'
        if 'age_limits' in group_data:
            new_group.age_limits = group_data['age_limits']
        else:
            new_group.age_limits = 0
        if 'city' in group_data:
            new_group.city = group_data['city']['title']
        else:
            new_group.city = '--'
        if 'country' in group_data:
            new_group.country = group_data['country']['title']
        else:
            new_group.country = '--'
        if 'description' in group_data and group_data['description']:
            new_group.description = group_data['description']
        else:
            new_group.description = '--'
        if 'members_count' in group_data:
            new_group.members_count = group_data['members_count']
        else:
            new_group.members_count = '--'
        if 'public_date_label' in group_data:
            new_group.public_date_label = group_data['public_date_label']
        else:
            new_group.public_date_label = '--'
        if 'site' in group_data and group_data['site']:
            new_group.site = group_data['site']
        else:
            new_group.site = '--'
        if 'status' in group_data and group_data['status']:
            new_group.status = group_data['status']
        else:
            new_group.status = '--'
        if 'verified' in group_data:
            new_group.verified = bool(group_data['verified'])
        else:
            new_group.verified = '--'
        if 'wiki_page' in group_data and group_data['wiki_page']:
            new_group.wiki_page = group_data['wiki_page']
        else:
            new_group.wiki_page = '--'
        new_group.wall_update_date = time.ctime(time.time())
        new_group.vec_update_date = "--"
        self.send_to_base(new_group)
        if type(group_posts) != str:
            self.write_posts_and_walls(new_group.base_id, new_group.wall_update_date, group_posts)

    def write_posts_and_walls(self, group_id, posts_get_date, posts_list):
        for post in posts_list:
            new_post = Posts()
            # new_post.post_id = random.randint(0, 999)
            new_post.text = str(post['text'])
            self.send_to_base(new_post)
            new_wall = Wall()
            # new_wall.wall_id = random.randint(0, 999)
            new_wall.gr_post_id = new_post.post_id
            new_wall.group_id = group_id
            new_wall.wall_update_date = posts_get_date
            self.send_to_base(new_wall)

    def get_blasclist(self):
        blacklist = []
        return blacklist

    def write_vec_story(self, group_id, vec):
        vec_update_date = time.ctime(time.time())
        new_vec = Vecs_Story()
        # new_vec.vec_id = random.randint(0, 999)
        new_vec.group_id = group_id
        new_vec.vec_update_date = vec_update_date
        if type(vec) != type(-1):
            new_vec.no_vec = False
        else:
            new_vec.no_vec = True
            vec = []
            for each in range(300):
                vec.append(0)
        new_vec.v1 = vec[0]
        new_vec.v2 = vec[1]
        new_vec.v3 = vec[2]
        new_vec.v4 = vec[3]
        new_vec.v5 = vec[4]
        new_vec.v6 = vec[5]
        new_vec.v7 = vec[6]
        new_vec.v8 = vec[7]
        new_vec.v9 = vec[8]
        new_vec.v10 = vec[9]
        new_vec.v11 = vec[10]
        new_vec.v12 = vec[11]
        new_vec.v13 = vec[12]
        new_vec.v14 = vec[13]
        new_vec.v15 = vec[14]
        new_vec.v16 = vec[15]
        new_vec.v17 = vec[16]
        new_vec.v18 = vec[17]
        new_vec.v19 = vec[18]
        new_vec.v20 = vec[19]
        new_vec.v21 = vec[20]
        new_vec.v22 = vec[21]
        new_vec.v23 = vec[22]
        new_vec.v24 = vec[23]
        new_vec.v25 = vec[24]
        new_vec.v26 = vec[25]
        new_vec.v27 = vec[26]
        new_vec.v28 = vec[27]
        new_vec.v29 = vec[28]
        new_vec.v30 = vec[29]
        new_vec.v31 = vec[30]
        new_vec.v32 = vec[31]
        new_vec.v33 = vec[32]
        new_vec.v34 = vec[33]
        new_vec.v35 = vec[34]
        new_vec.v36 = vec[35]
        new_vec.v37 = vec[36]
        new_vec.v38 = vec[37]
        new_vec.v39 = vec[38]
        new_vec.v40 = vec[39]
        new_vec.v41 = vec[40]
        new_vec.v42 = vec[41]
        new_vec.v43 = vec[42]
        new_vec.v44 = vec[43]
        new_vec.v45 = vec[44]
        new_vec.v46 = vec[45]
        new_vec.v47 = vec[46]
        new_vec.v48 = vec[47]
        new_vec.v49 = vec[48]
        new_vec.v50 = vec[49]
        new_vec.v51 = vec[50]
        new_vec.v52 = vec[51]
        new_vec.v53 = vec[52]
        new_vec.v54 = vec[53]
        new_vec.v55 = vec[54]
        new_vec.v56 = vec[55]
        new_vec.v57 = vec[56]
        new_vec.v58 = vec[57]
        new_vec.v59 = vec[58]
        new_vec.v60 = vec[59]
        new_vec.v61 = vec[60]
        new_vec.v62 = vec[61]
        new_vec.v63 = vec[62]
        new_vec.v64 = vec[63]
        new_vec.v65 = vec[64]
        new_vec.v66 = vec[65]
        new_vec.v67 = vec[66]
        new_vec.v68 = vec[67]
        new_vec.v69 = vec[68]
        new_vec.v70 = vec[69]
        new_vec.v71 = vec[70]
        new_vec.v72 = vec[71]
        new_vec.v73 = vec[72]
        new_vec.v74 = vec[73]
        new_vec.v75 = vec[74]
        new_vec.v76 = vec[75]
        new_vec.v77 = vec[76]
        new_vec.v78 = vec[77]
        new_vec.v79 = vec[78]
        new_vec.v80 = vec[79]
        new_vec.v81 = vec[80]
        new_vec.v82 = vec[81]
        new_vec.v83 = vec[82]
        new_vec.v84 = vec[83]
        new_vec.v85 = vec[84]
        new_vec.v86 = vec[85]
        new_vec.v87 = vec[86]
        new_vec.v88 = vec[87]
        new_vec.v89 = vec[88]
        new_vec.v90 = vec[89]
        new_vec.v91 = vec[90]
        new_vec.v92 = vec[91]
        new_vec.v93 = vec[92]
        new_vec.v94 = vec[93]
        new_vec.v95 = vec[94]
        new_vec.v96 = vec[95]
        new_vec.v97 = vec[96]
        new_vec.v98 = vec[97]
        new_vec.v99 = vec[98]
        new_vec.v100 = vec[99]
        new_vec.v101 = vec[100]
        new_vec.v102 = vec[101]
        new_vec.v103 = vec[102]
        new_vec.v104 = vec[103]
        new_vec.v105 = vec[104]
        new_vec.v106 = vec[105]
        new_vec.v107 = vec[106]
        new_vec.v108 = vec[107]
        new_vec.v109 = vec[108]
        new_vec.v110 = vec[109]
        new_vec.v111 = vec[110]
        new_vec.v112 = vec[111]
        new_vec.v113 = vec[112]
        new_vec.v114 = vec[113]
        new_vec.v115 = vec[114]
        new_vec.v116 = vec[115]
        new_vec.v117 = vec[116]
        new_vec.v118 = vec[117]
        new_vec.v119 = vec[118]
        new_vec.v120 = vec[119]
        new_vec.v121 = vec[120]
        new_vec.v122 = vec[121]
        new_vec.v123 = vec[122]
        new_vec.v124 = vec[123]
        new_vec.v125 = vec[124]
        new_vec.v126 = vec[125]
        new_vec.v127 = vec[126]
        new_vec.v128 = vec[127]
        new_vec.v129 = vec[128]
        new_vec.v130 = vec[129]
        new_vec.v131 = vec[130]
        new_vec.v132 = vec[131]
        new_vec.v133 = vec[132]
        new_vec.v134 = vec[133]
        new_vec.v135 = vec[134]
        new_vec.v136 = vec[135]
        new_vec.v137 = vec[136]
        new_vec.v138 = vec[137]
        new_vec.v139 = vec[138]
        new_vec.v140 = vec[139]
        new_vec.v141 = vec[140]
        new_vec.v142 = vec[141]
        new_vec.v143 = vec[142]
        new_vec.v144 = vec[143]
        new_vec.v145 = vec[144]
        new_vec.v146 = vec[145]
        new_vec.v147 = vec[146]
        new_vec.v148 = vec[147]
        new_vec.v149 = vec[148]
        new_vec.v150 = vec[149]
        new_vec.v151 = vec[150]
        new_vec.v152 = vec[151]
        new_vec.v153 = vec[152]
        new_vec.v154 = vec[153]
        new_vec.v155 = vec[154]
        new_vec.v156 = vec[155]
        new_vec.v157 = vec[156]
        new_vec.v158 = vec[157]
        new_vec.v159 = vec[158]
        new_vec.v160 = vec[159]
        new_vec.v161 = vec[160]
        new_vec.v162 = vec[161]
        new_vec.v163 = vec[162]
        new_vec.v164 = vec[163]
        new_vec.v165 = vec[164]
        new_vec.v166 = vec[165]
        new_vec.v167 = vec[166]
        new_vec.v168 = vec[167]
        new_vec.v169 = vec[168]
        new_vec.v170 = vec[169]
        new_vec.v171 = vec[170]
        new_vec.v172 = vec[171]
        new_vec.v173 = vec[172]
        new_vec.v174 = vec[173]
        new_vec.v175 = vec[174]
        new_vec.v176 = vec[175]
        new_vec.v177 = vec[176]
        new_vec.v178 = vec[177]
        new_vec.v179 = vec[178]
        new_vec.v180 = vec[179]
        new_vec.v181 = vec[180]
        new_vec.v182 = vec[181]
        new_vec.v183 = vec[182]
        new_vec.v184 = vec[183]
        new_vec.v185 = vec[184]
        new_vec.v186 = vec[185]
        new_vec.v187 = vec[186]
        new_vec.v188 = vec[187]
        new_vec.v189 = vec[188]
        new_vec.v190 = vec[189]
        new_vec.v191 = vec[190]
        new_vec.v192 = vec[191]
        new_vec.v193 = vec[192]
        new_vec.v194 = vec[193]
        new_vec.v195 = vec[194]
        new_vec.v196 = vec[195]
        new_vec.v197 = vec[196]
        new_vec.v198 = vec[197]
        new_vec.v199 = vec[198]
        new_vec.v200 = vec[199]
        new_vec.v201 = vec[200]
        new_vec.v202 = vec[201]
        new_vec.v203 = vec[202]
        new_vec.v204 = vec[203]
        new_vec.v205 = vec[204]
        new_vec.v206 = vec[205]
        new_vec.v207 = vec[206]
        new_vec.v208 = vec[207]
        new_vec.v209 = vec[208]
        new_vec.v210 = vec[209]
        new_vec.v211 = vec[210]
        new_vec.v212 = vec[211]
        new_vec.v213 = vec[212]
        new_vec.v214 = vec[213]
        new_vec.v215 = vec[214]
        new_vec.v216 = vec[215]
        new_vec.v217 = vec[216]
        new_vec.v218 = vec[217]
        new_vec.v219 = vec[218]
        new_vec.v220 = vec[219]
        new_vec.v221 = vec[220]
        new_vec.v222 = vec[221]
        new_vec.v223 = vec[222]
        new_vec.v224 = vec[223]
        new_vec.v225 = vec[224]
        new_vec.v226 = vec[225]
        new_vec.v227 = vec[226]
        new_vec.v228 = vec[227]
        new_vec.v229 = vec[228]
        new_vec.v230 = vec[229]
        new_vec.v231 = vec[230]
        new_vec.v232 = vec[231]
        new_vec.v233 = vec[232]
        new_vec.v234 = vec[233]
        new_vec.v235 = vec[234]
        new_vec.v236 = vec[235]
        new_vec.v237 = vec[236]
        new_vec.v238 = vec[237]
        new_vec.v239 = vec[238]
        new_vec.v240 = vec[239]
        new_vec.v241 = vec[240]
        new_vec.v242 = vec[241]
        new_vec.v243 = vec[242]
        new_vec.v244 = vec[243]
        new_vec.v245 = vec[244]
        new_vec.v246 = vec[245]
        new_vec.v247 = vec[246]
        new_vec.v248 = vec[247]
        new_vec.v249 = vec[248]
        new_vec.v250 = vec[249]
        new_vec.v251 = vec[250]
        new_vec.v252 = vec[251]
        new_vec.v253 = vec[252]
        new_vec.v254 = vec[253]
        new_vec.v255 = vec[254]
        new_vec.v256 = vec[255]
        new_vec.v257 = vec[256]
        new_vec.v258 = vec[257]
        new_vec.v259 = vec[258]
        new_vec.v260 = vec[259]
        new_vec.v261 = vec[260]
        new_vec.v262 = vec[261]
        new_vec.v263 = vec[262]
        new_vec.v264 = vec[263]
        new_vec.v265 = vec[264]
        new_vec.v266 = vec[265]
        new_vec.v267 = vec[266]
        new_vec.v268 = vec[267]
        new_vec.v269 = vec[268]
        new_vec.v270 = vec[269]
        new_vec.v271 = vec[270]
        new_vec.v272 = vec[271]
        new_vec.v273 = vec[272]
        new_vec.v274 = vec[273]
        new_vec.v275 = vec[274]
        new_vec.v276 = vec[275]
        new_vec.v277 = vec[276]
        new_vec.v278 = vec[277]
        new_vec.v279 = vec[278]
        new_vec.v280 = vec[279]
        new_vec.v281 = vec[280]
        new_vec.v282 = vec[281]
        new_vec.v283 = vec[282]
        new_vec.v284 = vec[283]
        new_vec.v285 = vec[284]
        new_vec.v286 = vec[285]
        new_vec.v287 = vec[286]
        new_vec.v288 = vec[287]
        new_vec.v289 = vec[288]
        new_vec.v290 = vec[289]
        new_vec.v291 = vec[290]
        new_vec.v292 = vec[291]
        new_vec.v293 = vec[292]
        new_vec.v294 = vec[293]
        new_vec.v295 = vec[294]
        new_vec.v296 = vec[295]
        new_vec.v297 = vec[296]
        new_vec.v298 = vec[297]
        new_vec.v299 = vec[298]
        new_vec.v300 = vec[299]
        self.send_to_base(new_vec)

    def send_to_base(self, object):
        self.session.add(object)
        self.session.commit()

    def close(self):
        self.session.close()

    def get_walls(self):
        gr = self.session.query(Groups).all()
        # posts = self.session.query(Posts).all()
        walls = self.session.query(Wall).all()
        result = {}
        for group in gr:
            select_walls = 'select gr_post_id from Wall WHERE group_id = ' + str(group.base_id)
            select_posts = 'select * from Posts WHERE post_id in (' + select_walls + ")"
            sql_posts = self.session.execute(select_posts).fetchall()
            posts = []
            for sql_post in sql_posts:
                post = sql_post._row[1]
                posts.append(post)
            result[group.base_id] = posts
        return result

    def get_vecs(self):
        vecs = {}
        gr = self.session.query(Groups).all()
        for group in gr:
            """select_vecs = 'select group_id, ... from Vec_Story where group_id = ' + str(
                group.base_id) + ' and vec_update_date = ' + str(group.vec_update_date)"""
            select_vecs = 'SELECT * from Vec_Story WHERE group_id = ' + str(group.base_id)
            vec = self.session.execute(select_vecs).fetchall()
            if type(vec) == list:
                vec = vec[-1]
            if vec.no_vec:
                continue
            value = []
            value.append(vec.v1)
            value.append(vec.v2)
            value.append(vec.v3)
            value.append(vec.v4)
            value.append(vec.v5)
            value.append(vec.v6)
            value.append(vec.v7)
            value.append(vec.v8)
            value.append(vec.v9)
            value.append(vec.v10)
            value.append(vec.v11)
            value.append(vec.v12)
            value.append(vec.v13)
            value.append(vec.v14)
            value.append(vec.v15)
            value.append(vec.v16)
            value.append(vec.v17)
            value.append(vec.v18)
            value.append(vec.v19)
            value.append(vec.v20)
            value.append(vec.v21)
            value.append(vec.v22)
            value.append(vec.v23)
            value.append(vec.v24)
            value.append(vec.v25)
            value.append(vec.v26)
            value.append(vec.v27)
            value.append(vec.v28)
            value.append(vec.v29)
            value.append(vec.v30)
            value.append(vec.v31)
            value.append(vec.v32)
            value.append(vec.v33)
            value.append(vec.v34)
            value.append(vec.v35)
            value.append(vec.v36)
            value.append(vec.v37)
            value.append(vec.v38)
            value.append(vec.v39)
            value.append(vec.v40)
            value.append(vec.v41)
            value.append(vec.v42)
            value.append(vec.v43)
            value.append(vec.v44)
            value.append(vec.v45)
            value.append(vec.v46)
            value.append(vec.v47)
            value.append(vec.v48)
            value.append(vec.v49)
            value.append(vec.v50)
            value.append(vec.v51)
            value.append(vec.v52)
            value.append(vec.v53)
            value.append(vec.v54)
            value.append(vec.v55)
            value.append(vec.v56)
            value.append(vec.v57)
            value.append(vec.v58)
            value.append(vec.v59)
            value.append(vec.v60)
            value.append(vec.v61)
            value.append(vec.v62)
            value.append(vec.v63)
            value.append(vec.v64)
            value.append(vec.v65)
            value.append(vec.v66)
            value.append(vec.v67)
            value.append(vec.v68)
            value.append(vec.v69)
            value.append(vec.v70)
            value.append(vec.v71)
            value.append(vec.v72)
            value.append(vec.v73)
            value.append(vec.v74)
            value.append(vec.v75)
            value.append(vec.v76)
            value.append(vec.v77)
            value.append(vec.v78)
            value.append(vec.v79)
            value.append(vec.v80)
            value.append(vec.v81)
            value.append(vec.v82)
            value.append(vec.v83)
            value.append(vec.v84)
            value.append(vec.v85)
            value.append(vec.v86)
            value.append(vec.v87)
            value.append(vec.v88)
            value.append(vec.v89)
            value.append(vec.v90)
            value.append(vec.v91)
            value.append(vec.v92)
            value.append(vec.v93)
            value.append(vec.v94)
            value.append(vec.v95)
            value.append(vec.v96)
            value.append(vec.v97)
            value.append(vec.v98)
            value.append(vec.v99)
            value.append(vec.v100)
            value.append(vec.v101)
            value.append(vec.v102)
            value.append(vec.v103)
            value.append(vec.v104)
            value.append(vec.v105)
            value.append(vec.v106)
            value.append(vec.v107)
            value.append(vec.v108)
            value.append(vec.v109)
            value.append(vec.v110)
            value.append(vec.v111)
            value.append(vec.v112)
            value.append(vec.v113)
            value.append(vec.v114)
            value.append(vec.v115)
            value.append(vec.v116)
            value.append(vec.v117)
            value.append(vec.v118)
            value.append(vec.v119)
            value.append(vec.v120)
            value.append(vec.v121)
            value.append(vec.v122)
            value.append(vec.v123)
            value.append(vec.v124)
            value.append(vec.v125)
            value.append(vec.v126)
            value.append(vec.v127)
            value.append(vec.v128)
            value.append(vec.v129)
            value.append(vec.v130)
            value.append(vec.v131)
            value.append(vec.v132)
            value.append(vec.v133)
            value.append(vec.v134)
            value.append(vec.v135)
            value.append(vec.v136)
            value.append(vec.v137)
            value.append(vec.v138)
            value.append(vec.v139)
            value.append(vec.v140)
            value.append(vec.v141)
            value.append(vec.v142)
            value.append(vec.v143)
            value.append(vec.v144)
            value.append(vec.v145)
            value.append(vec.v146)
            value.append(vec.v147)
            value.append(vec.v148)
            value.append(vec.v149)
            value.append(vec.v150)
            value.append(vec.v151)
            value.append(vec.v152)
            value.append(vec.v153)
            value.append(vec.v154)
            value.append(vec.v155)
            value.append(vec.v156)
            value.append(vec.v157)
            value.append(vec.v158)
            value.append(vec.v159)
            value.append(vec.v160)
            value.append(vec.v161)
            value.append(vec.v162)
            value.append(vec.v163)
            value.append(vec.v164)
            value.append(vec.v165)
            value.append(vec.v166)
            value.append(vec.v167)
            value.append(vec.v168)
            value.append(vec.v169)
            value.append(vec.v170)
            value.append(vec.v171)
            value.append(vec.v172)
            value.append(vec.v173)
            value.append(vec.v174)
            value.append(vec.v175)
            value.append(vec.v176)
            value.append(vec.v177)
            value.append(vec.v178)
            value.append(vec.v179)
            value.append(vec.v180)
            value.append(vec.v181)
            value.append(vec.v182)
            value.append(vec.v183)
            value.append(vec.v184)
            value.append(vec.v185)
            value.append(vec.v186)
            value.append(vec.v187)
            value.append(vec.v188)
            value.append(vec.v189)
            value.append(vec.v190)
            value.append(vec.v191)
            value.append(vec.v192)
            value.append(vec.v193)
            value.append(vec.v194)
            value.append(vec.v195)
            value.append(vec.v196)
            value.append(vec.v197)
            value.append(vec.v198)
            value.append(vec.v199)
            value.append(vec.v200)
            value.append(vec.v201)
            value.append(vec.v202)
            value.append(vec.v203)
            value.append(vec.v204)
            value.append(vec.v205)
            value.append(vec.v206)
            value.append(vec.v207)
            value.append(vec.v208)
            value.append(vec.v209)
            value.append(vec.v210)
            value.append(vec.v211)
            value.append(vec.v212)
            value.append(vec.v213)
            value.append(vec.v214)
            value.append(vec.v215)
            value.append(vec.v216)
            value.append(vec.v217)
            value.append(vec.v218)
            value.append(vec.v219)
            value.append(vec.v220)
            value.append(vec.v221)
            value.append(vec.v222)
            value.append(vec.v223)
            value.append(vec.v224)
            value.append(vec.v225)
            value.append(vec.v226)
            value.append(vec.v227)
            value.append(vec.v228)
            value.append(vec.v229)
            value.append(vec.v230)
            value.append(vec.v231)
            value.append(vec.v232)
            value.append(vec.v233)
            value.append(vec.v234)
            value.append(vec.v235)
            value.append(vec.v236)
            value.append(vec.v237)
            value.append(vec.v238)
            value.append(vec.v239)
            value.append(vec.v240)
            value.append(vec.v241)
            value.append(vec.v242)
            value.append(vec.v243)
            value.append(vec.v244)
            value.append(vec.v245)
            value.append(vec.v246)
            value.append(vec.v247)
            value.append(vec.v248)
            value.append(vec.v249)
            value.append(vec.v250)
            value.append(vec.v251)
            value.append(vec.v252)
            value.append(vec.v253)
            value.append(vec.v254)
            value.append(vec.v255)
            value.append(vec.v256)
            value.append(vec.v257)
            value.append(vec.v258)
            value.append(vec.v259)
            value.append(vec.v260)
            value.append(vec.v261)
            value.append(vec.v262)
            value.append(vec.v263)
            value.append(vec.v264)
            value.append(vec.v265)
            value.append(vec.v266)
            value.append(vec.v267)
            value.append(vec.v268)
            value.append(vec.v269)
            value.append(vec.v270)
            value.append(vec.v271)
            value.append(vec.v272)
            value.append(vec.v273)
            value.append(vec.v274)
            value.append(vec.v275)
            value.append(vec.v276)
            value.append(vec.v277)
            value.append(vec.v278)
            value.append(vec.v279)
            value.append(vec.v280)
            value.append(vec.v281)
            value.append(vec.v282)
            value.append(vec.v283)
            value.append(vec.v284)
            value.append(vec.v285)
            value.append(vec.v286)
            value.append(vec.v287)
            value.append(vec.v288)
            value.append(vec.v289)
            value.append(vec.v290)
            value.append(vec.v291)
            value.append(vec.v292)
            value.append(vec.v293)
            value.append(vec.v294)
            value.append(vec.v295)
            value.append(vec.v296)
            value.append(vec.v297)
            value.append(vec.v298)
            value.append(vec.v299)
            value.append(vec.v300)
            value = tuple(value)
            vecs[group.base_id] = value
        return vecs

    def get_groups_data(self, id_list):
        sql_groups = {}
        #select_groups = 'select * from Groups WHERE base_id in ' + str(id_list)
        #select_groups = 'SELECT * from GROUP'
        #sql_groups = self.session.execute(select_groups).fetchall()
        gr = self.session.query(Groups).all()
        for group in gr:
            if group.base_id in id_list:
                sql_groups[group.base_id]=group
        return sql_groups


class Groups(Base):
    __tablename__ = "Group"
    base_id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(Integer)
    link = Column(String(Link_len))
    # ____________Main_info_________________
    name = Column(String(Name_len))
    screen_name = Column(String(Name_len))
    is_closed = Column(Boolean)
    deactivated = Column(Boolean)
    group_type = Column(String(Type_len))
    photo_50 = Column(String(Link_len))
    photo_100 = Column(String(Link_len))
    photo_200 = Column(String(Link_len))
    # ___________Add_info____________________
    activity = Column(String(Activity_string_len))
    age_limits = Column(Integer)
    city = Column(String(City_name_len))
    country = Column(String(Country_name_len))
    description = Column(String(Description_len))
    members_count = Column(Integer)
    public_date_label = Column(String(Date_string_len))
    site = Column(String(Link_len))
    status = Column(String(Status_len))
    verified = Column(Boolean)
    wiki_page = Column(String(Link_len))
    # __________Updates______________________
    wall_update_date = Column(String(Date_string_len))  # ForeignKey(Wall.wall_update_date)
    vec_update_date = Column(String(Date_string_len))  # ForeignKey(Vecs_Story.vec_update_date)

    def __repr__(self):
        return "<Group(" + " ".join(
            [str(self.base_id), str(self.vk_id), self.link, self.name, self.screen_name, str(self.is_closed),
             str(self.deactivated), self.group_type, self.photo_50, self.photo_100, self.photo_200,
             self.activity, str(self.age_limits), self.city, self.country, self.description,
             str(self.members_count), self.public_date_label,
             self.site, self.status, str(self.verified), self.wiki_page, self.wall_update_date,
             self.vec_update_date]) + ")>"  # (%i,%i,%r,%r,%r,%i,%i,%r,%i,%r,%r,%r,%r,%i,%r,%r,%r,%i,%r,%r,%r,%i,%r,%r,%r)


class Posts(Base):  # !!!!!!
    __tablename__ = "Posts"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(Post_len))

    def __repr__(self):
        return "<Post(%i, %r)>" % (self.post_id, self.text)


class Wall(Base):
    __tablename__ = "Wall"
    wall_id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey(Groups.base_id))
    wall_update_date = Column(String(Date_string_len))
    gr_post_id = Column(String(Post_len), ForeignKey(Posts.post_id))

    def __repr__(self):
        return "<Wall(%i, %i, %r, %i)>" % (self.wall_id, self.group_id, self.wall_update_date, self.gr_post_id)


class Vecs_Story(Base):
    __tablename__ = "Vec_Story"
    vec_id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey(Groups.base_id))
    vec_update_date = Column(String(Date_string_len))
    no_vec = Column(Boolean)
    v1 = Column(Integer)
    v2 = Column(Integer)
    v3 = Column(Integer)
    v4 = Column(Integer)
    v5 = Column(Integer)
    v6 = Column(Integer)
    v7 = Column(Integer)
    v8 = Column(Integer)
    v9 = Column(Integer)
    v10 = Column(Integer)
    v11 = Column(Integer)
    v12 = Column(Integer)
    v13 = Column(Integer)
    v14 = Column(Integer)
    v15 = Column(Integer)
    v16 = Column(Integer)
    v17 = Column(Integer)
    v18 = Column(Integer)
    v19 = Column(Integer)
    v20 = Column(Integer)
    v21 = Column(Integer)
    v22 = Column(Integer)
    v23 = Column(Integer)
    v24 = Column(Integer)
    v25 = Column(Integer)
    v26 = Column(Integer)
    v27 = Column(Integer)
    v28 = Column(Integer)
    v29 = Column(Integer)
    v30 = Column(Integer)
    v31 = Column(Integer)
    v32 = Column(Integer)
    v33 = Column(Integer)
    v34 = Column(Integer)
    v35 = Column(Integer)
    v36 = Column(Integer)
    v37 = Column(Integer)
    v38 = Column(Integer)
    v39 = Column(Integer)
    v40 = Column(Integer)
    v41 = Column(Integer)
    v42 = Column(Integer)
    v43 = Column(Integer)
    v44 = Column(Integer)
    v45 = Column(Integer)
    v46 = Column(Integer)
    v47 = Column(Integer)
    v48 = Column(Integer)
    v49 = Column(Integer)
    v50 = Column(Integer)
    v51 = Column(Integer)
    v52 = Column(Integer)
    v53 = Column(Integer)
    v54 = Column(Integer)
    v55 = Column(Integer)
    v56 = Column(Integer)
    v57 = Column(Integer)
    v58 = Column(Integer)
    v59 = Column(Integer)
    v60 = Column(Integer)
    v61 = Column(Integer)
    v62 = Column(Integer)
    v63 = Column(Integer)
    v64 = Column(Integer)
    v65 = Column(Integer)
    v66 = Column(Integer)
    v67 = Column(Integer)
    v68 = Column(Integer)
    v69 = Column(Integer)
    v70 = Column(Integer)
    v71 = Column(Integer)
    v72 = Column(Integer)
    v73 = Column(Integer)
    v74 = Column(Integer)
    v75 = Column(Integer)
    v76 = Column(Integer)
    v77 = Column(Integer)
    v78 = Column(Integer)
    v79 = Column(Integer)
    v80 = Column(Integer)
    v81 = Column(Integer)
    v82 = Column(Integer)
    v83 = Column(Integer)
    v84 = Column(Integer)
    v85 = Column(Integer)
    v86 = Column(Integer)
    v87 = Column(Integer)
    v88 = Column(Integer)
    v89 = Column(Integer)
    v90 = Column(Integer)
    v91 = Column(Integer)
    v92 = Column(Integer)
    v93 = Column(Integer)
    v94 = Column(Integer)
    v95 = Column(Integer)
    v96 = Column(Integer)
    v97 = Column(Integer)
    v98 = Column(Integer)
    v99 = Column(Integer)
    v100 = Column(Integer)
    v101 = Column(Integer)
    v102 = Column(Integer)
    v103 = Column(Integer)
    v104 = Column(Integer)
    v105 = Column(Integer)
    v106 = Column(Integer)
    v107 = Column(Integer)
    v108 = Column(Integer)
    v109 = Column(Integer)
    v110 = Column(Integer)
    v111 = Column(Integer)
    v112 = Column(Integer)
    v113 = Column(Integer)
    v114 = Column(Integer)
    v115 = Column(Integer)
    v116 = Column(Integer)
    v117 = Column(Integer)
    v118 = Column(Integer)
    v119 = Column(Integer)
    v120 = Column(Integer)
    v121 = Column(Integer)
    v122 = Column(Integer)
    v123 = Column(Integer)
    v124 = Column(Integer)
    v125 = Column(Integer)
    v126 = Column(Integer)
    v127 = Column(Integer)
    v128 = Column(Integer)
    v129 = Column(Integer)
    v130 = Column(Integer)
    v131 = Column(Integer)
    v132 = Column(Integer)
    v133 = Column(Integer)
    v134 = Column(Integer)
    v135 = Column(Integer)
    v136 = Column(Integer)
    v137 = Column(Integer)
    v138 = Column(Integer)
    v139 = Column(Integer)
    v140 = Column(Integer)
    v141 = Column(Integer)
    v142 = Column(Integer)
    v143 = Column(Integer)
    v144 = Column(Integer)
    v145 = Column(Integer)
    v146 = Column(Integer)
    v147 = Column(Integer)
    v148 = Column(Integer)
    v149 = Column(Integer)
    v150 = Column(Integer)
    v151 = Column(Integer)
    v152 = Column(Integer)
    v153 = Column(Integer)
    v154 = Column(Integer)
    v155 = Column(Integer)
    v156 = Column(Integer)
    v157 = Column(Integer)
    v158 = Column(Integer)
    v159 = Column(Integer)
    v160 = Column(Integer)
    v161 = Column(Integer)
    v162 = Column(Integer)
    v163 = Column(Integer)
    v164 = Column(Integer)
    v165 = Column(Integer)
    v166 = Column(Integer)
    v167 = Column(Integer)
    v168 = Column(Integer)
    v169 = Column(Integer)
    v170 = Column(Integer)
    v171 = Column(Integer)
    v172 = Column(Integer)
    v173 = Column(Integer)
    v174 = Column(Integer)
    v175 = Column(Integer)
    v176 = Column(Integer)
    v177 = Column(Integer)
    v178 = Column(Integer)
    v179 = Column(Integer)
    v180 = Column(Integer)
    v181 = Column(Integer)
    v182 = Column(Integer)
    v183 = Column(Integer)
    v184 = Column(Integer)
    v185 = Column(Integer)
    v186 = Column(Integer)
    v187 = Column(Integer)
    v188 = Column(Integer)
    v189 = Column(Integer)
    v190 = Column(Integer)
    v191 = Column(Integer)
    v192 = Column(Integer)
    v193 = Column(Integer)
    v194 = Column(Integer)
    v195 = Column(Integer)
    v196 = Column(Integer)
    v197 = Column(Integer)
    v198 = Column(Integer)
    v199 = Column(Integer)
    v200 = Column(Integer)
    v201 = Column(Integer)
    v202 = Column(Integer)
    v203 = Column(Integer)
    v204 = Column(Integer)
    v205 = Column(Integer)
    v206 = Column(Integer)
    v207 = Column(Integer)
    v208 = Column(Integer)
    v209 = Column(Integer)
    v210 = Column(Integer)
    v211 = Column(Integer)
    v212 = Column(Integer)
    v213 = Column(Integer)
    v214 = Column(Integer)
    v215 = Column(Integer)
    v216 = Column(Integer)
    v217 = Column(Integer)
    v218 = Column(Integer)
    v219 = Column(Integer)
    v220 = Column(Integer)
    v221 = Column(Integer)
    v222 = Column(Integer)
    v223 = Column(Integer)
    v224 = Column(Integer)
    v225 = Column(Integer)
    v226 = Column(Integer)
    v227 = Column(Integer)
    v228 = Column(Integer)
    v229 = Column(Integer)
    v230 = Column(Integer)
    v231 = Column(Integer)
    v232 = Column(Integer)
    v233 = Column(Integer)
    v234 = Column(Integer)
    v235 = Column(Integer)
    v236 = Column(Integer)
    v237 = Column(Integer)
    v238 = Column(Integer)
    v239 = Column(Integer)
    v240 = Column(Integer)
    v241 = Column(Integer)
    v242 = Column(Integer)
    v243 = Column(Integer)
    v244 = Column(Integer)
    v245 = Column(Integer)
    v246 = Column(Integer)
    v247 = Column(Integer)
    v248 = Column(Integer)
    v249 = Column(Integer)
    v250 = Column(Integer)
    v251 = Column(Integer)
    v252 = Column(Integer)
    v253 = Column(Integer)
    v254 = Column(Integer)
    v255 = Column(Integer)
    v256 = Column(Integer)
    v257 = Column(Integer)
    v258 = Column(Integer)
    v259 = Column(Integer)
    v260 = Column(Integer)
    v261 = Column(Integer)
    v262 = Column(Integer)
    v263 = Column(Integer)
    v264 = Column(Integer)
    v265 = Column(Integer)
    v266 = Column(Integer)
    v267 = Column(Integer)
    v268 = Column(Integer)
    v269 = Column(Integer)
    v270 = Column(Integer)
    v271 = Column(Integer)
    v272 = Column(Integer)
    v273 = Column(Integer)
    v274 = Column(Integer)
    v275 = Column(Integer)
    v276 = Column(Integer)
    v277 = Column(Integer)
    v278 = Column(Integer)
    v279 = Column(Integer)
    v280 = Column(Integer)
    v281 = Column(Integer)
    v282 = Column(Integer)
    v283 = Column(Integer)
    v284 = Column(Integer)
    v285 = Column(Integer)
    v286 = Column(Integer)
    v287 = Column(Integer)
    v288 = Column(Integer)
    v289 = Column(Integer)
    v290 = Column(Integer)
    v291 = Column(Integer)
    v292 = Column(Integer)
    v293 = Column(Integer)
    v294 = Column(Integer)
    v295 = Column(Integer)
    v296 = Column(Integer)
    v297 = Column(Integer)
    v298 = Column(Integer)
    v299 = Column(Integer)
    v300 = Column(Integer)

    def __repr__(self):
        return "<Vec_story(" + ",".join(
            [
                self.vec_id, self.group_id, self.vec_update_date + str(self.no_vec), str(self.v0), str(self.v1),
                str(self.v2), str(self.v3), str(self.v4), str(self.v5), str(self.v6), str(self.v7), str(self.v8),
                str(self.v9), str(self.v10), str(self.v11), str(self.v12), str(self.v13), str(self.v14), str(self.v15),
                str(self.v16), str(self.v17), str(self.v18), str(self.v19), str(self.v20), str(self.v21), str(self.v22),
                str(self.v23), str(self.v24), str(self.v25), str(self.v26), str(self.v27), str(self.v28), str(self.v29),
                str(self.v30), str(self.v31), str(self.v32), str(self.v33), str(self.v34), str(self.v35), str(self.v36),
                str(self.v37), str(self.v38), str(self.v39), str(self.v40), str(self.v41), str(self.v42), str(self.v43),
                str(self.v44), str(self.v45), str(self.v46), str(self.v47), str(self.v48), str(self.v49), str(self.v50),
                str(self.v51), str(self.v52), str(self.v53), str(self.v54), str(self.v55), str(self.v56), str(self.v57),
                str(self.v58), str(self.v59), str(self.v60), str(self.v61), str(self.v62), str(self.v63), str(self.v64),
                str(self.v65), str(self.v66), str(self.v67), str(self.v68), str(self.v69), str(self.v70), str(self.v71),
                str(self.v72), str(self.v73), str(self.v74), str(self.v75), str(self.v76), str(self.v77), str(self.v78),
                str(self.v79), str(self.v80), str(self.v81), str(self.v82), str(self.v83), str(self.v84), str(self.v85),
                str(self.v86), str(self.v87), str(self.v88), str(self.v89), str(self.v90), str(self.v91), str(self.v92),
                str(self.v93), str(self.v94), str(self.v95), str(self.v96), str(self.v97), str(self.v98), str(self.v99),
                str(self.v100), str(self.v101), str(self.v102), str(self.v103), str(self.v104), str(self.v105),
                str(self.v106), str(self.v107), str(self.v108), str(self.v109), str(self.v110), str(self.v111),
                str(self.v112), str(self.v113), str(self.v114), str(self.v115), str(self.v116), str(self.v117),
                str(self.v118), str(self.v119), str(self.v120), str(self.v121), str(self.v122), str(self.v123),
                str(self.v124), str(self.v125), str(self.v126), str(self.v127), str(self.v128), str(self.v129),
                str(self.v130), str(self.v131), str(self.v132), str(self.v133), str(self.v134), str(self.v135),
                str(self.v136), str(self.v137), str(self.v138), str(self.v139), str(self.v140), str(self.v141),
                str(self.v142), str(self.v143), str(self.v144), str(self.v145), str(self.v146), str(self.v147),
                str(self.v148), str(self.v149), str(self.v150), str(self.v151), str(self.v152), str(self.v153),
                str(self.v154), str(self.v155), str(self.v156), str(self.v157), str(self.v158), str(self.v159),
                str(self.v160), str(self.v161), str(self.v162), str(self.v163), str(self.v164), str(self.v165),
                str(self.v166), str(self.v167), str(self.v168), str(self.v169), str(self.v170), str(self.v171),
                str(self.v172), str(self.v173), str(self.v174), str(self.v175), str(self.v176), str(self.v177),
                str(self.v178), str(self.v179), str(self.v180), str(self.v181), str(self.v182), str(self.v183),
                str(self.v184), str(self.v185), str(self.v186), str(self.v187), str(self.v188), str(self.v189),
                str(self.v190), str(self.v191), str(self.v192), str(self.v193), str(self.v194), str(self.v195),
                str(self.v196), str(self.v197), str(self.v198), str(self.v199), str(self.v200), str(self.v201),
                str(self.v202), str(self.v203), str(self.v204), str(self.v205), str(self.v206), str(self.v207),
                str(self.v208), str(self.v209), str(self.v210), str(self.v211), str(self.v212), str(self.v213),
                str(self.v214), str(self.v215), str(self.v216), str(self.v217), str(self.v218), str(self.v219),
                str(self.v220), str(self.v221), str(self.v222), str(self.v223), str(self.v224), str(self.v225),
                str(self.v226), str(self.v227), str(self.v228), str(self.v229), str(self.v230), str(self.v231),
                str(self.v232), str(self.v233), str(self.v234), str(self.v235), str(self.v236), str(self.v237),
                str(self.v238), str(self.v239), str(self.v240), str(self.v241), str(self.v242), str(self.v243),
                str(self.v244), str(self.v245), str(self.v246), str(self.v247), str(self.v248), str(self.v249),
                str(self.v250), str(self.v251), str(self.v252), str(self.v253), str(self.v254), str(self.v255),
                str(self.v256), str(self.v257), str(self.v258), str(self.v259), str(self.v260), str(self.v261),
                str(self.v262), str(self.v263), str(self.v264), str(self.v265), str(self.v266), str(self.v267),
                str(self.v268), str(self.v269), str(self.v270), str(self.v271), str(self.v272), str(self.v273),
                str(self.v274), str(self.v275), str(self.v276), str(self.v277), str(self.v278), str(self.v279),
                str(self.v280), str(self.v281), str(self.v282), str(self.v283), str(self.v284), str(self.v285),
                str(self.v286), str(self.v287), str(self.v288), str(self.v289), str(self.v290), str(self.v291),
                str(self.v292), str(self.v293), str(self.v294), str(self.v295), str(self.v296), str(self.v297),
                str(self.v298), str(self.v299), str(self.v300)
            ]) + ")>"


if __name__ == "__main__":
    pass