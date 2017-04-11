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
database_path = 'test.db'
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

    def write_group_to_base(self, group_data):
        new_group = Groups()
        new_group.base_id = random.randint(0, 9999)
        new_group.vk_id = group_data['id']
        new_group.link = "vk.com/" + str(group_data['id'])
        new_group.name = group_data['name']
        if 'screen_name' in group_data:
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
            new_group.age_limits = '--'
        if 'city' in group_data:
            new_group.city = group_data['city']
        else:
            new_group.city = '--'
        if 'country' in group_data:
            new_group.country = group_data['country']
        else:
            new_group.country = '--'
        if 'description' in group_data:
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
        if 'site' in group_data:
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
        if 'wiki_page' in group_data:
            new_group.wiki_page = group_data['wiki_page']
        else:
            new_group.wiki_page = '--'
        new_group.wall_update_date = "--"  # time.strftime()
        new_group.vec_update_date = "--"
        self.send_to_base(new_group)
        self.write_posts_and_walls(new_group.base_id, new_group.wall_update_date, posts)

    def write_posts_and_walls(self, group_id, posts_get_date, posts_list):
        for post in posts_list:
            new_post = Posts()
            new_post.post_id = random.randint(0, 999)
            new_post.text = post['text']
            self.send_to_base(new_post)
            new_wall = Wall()
            new_wall.wall_id = random.randint(0, 999)
            new_wall.gr_post_id = new_post.post_id
            new_wall.group_id = group_id
            new_wall.wall_update_date = posts_get_date
            self.send_to_base(new_wall)

    def get_blasclist(self):
        pass

    def write_vec_story(self, group_id, vec_update_date, vec):
        new_vec = Vecs_Story()
        new_vec.vec_id = random.randint(0, 999)
        new_vec.group_id = group_id
        new_vec.vec_update_date = vec_update_date
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


class Groups(Base):
    __tablename__ = "Group"
    base_id = Column(Integer, primary_key=True)
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
    post_id = Column(Integer, primary_key=True)
    text = Column(String(Post_len))

    def __repr__(self):
        return "<Post(%i, %r)>" % self.post_id, self.text


class Wall(Base):
    __tablename__ = "Wall"
    wall_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey(Groups.base_id))
    wall_update_date = Column(String(Date_string_len))
    gr_post_id = Column(String(Post_len), ForeignKey(Posts.post_id))

    def __repr__(self):
        return "<Post(%i, %i, %r, %i)>" % self.wall_id, self.group_id, self.wall_update_date, self.gr_post_id


class Vecs_Story(Base):
    __tablename__ = "Vec_Story"
    vec_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey(Groups.base_id))
    vec_update_date = Column(String(Date_string_len))
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
        return "<Post(" + ",".join(
            [self.vec_id, self.group_id, self.vec_update_date + self.v1, str(self.v0), str(self.v1), str(self.v2),
             str(self.v3), str(self.v4), str(self.v5), str(self.v6), str(self.v7), str(self.v8), str(self.v9),
             str(self.v10), str(self.v11), str(self.v12), str(self.v13), str(self.v14), str(self.v15), str(self.v16),
             str(self.v17), str(self.v18), str(self.v19), str(self.v20), str(self.v21), str(self.v22), str(self.v23),
             str(self.v24), str(self.v25), str(self.v26), str(self.v27), str(self.v28), str(self.v29), str(self.v30),
             str(self.v31), str(self.v32), str(self.v33), str(self.v34), str(self.v35), str(self.v36), str(self.v37),
             str(self.v38), str(self.v39), str(self.v40), str(self.v41), str(self.v42), str(self.v43), str(self.v44),
             str(self.v45), str(self.v46), str(self.v47), str(self.v48), str(self.v49), str(self.v50), str(self.v51),
             str(self.v52), str(self.v53), str(self.v54), str(self.v55), str(self.v56), str(self.v57), str(self.v58),
             str(self.v59), str(self.v60), str(self.v61), str(self.v62), str(self.v63), str(self.v64), str(self.v65),
             str(self.v66), str(self.v67), str(self.v68), str(self.v69), str(self.v70), str(self.v71), str(self.v72),
             str(self.v73), str(self.v74), str(self.v75), str(self.v76), str(self.v77), str(self.v78), str(self.v79),
             str(self.v80), str(self.v81), str(self.v82), str(self.v83), str(self.v84), str(self.v85), str(self.v86),
             str(self.v87), str(self.v88), str(self.v89), str(self.v90), str(self.v91), str(self.v92), str(self.v93),
             str(self.v94), str(self.v95), str(self.v96), str(self.v97), str(self.v98), str(self.v99), str(self.v100),
             str(self.v101), str(self.v102), str(self.v103), str(self.v104), str(self.v105), str(self.v106),
             str(self.v107), str(self.v108), str(self.v109), str(self.v110), str(self.v111), str(self.v112),
             str(self.v113), str(self.v114), str(self.v115), str(self.v116), str(self.v117), str(self.v118),
             str(self.v119), str(self.v120), str(self.v121), str(self.v122), str(self.v123), str(self.v124),
             str(self.v125), str(self.v126), str(self.v127), str(self.v128), str(self.v129), str(self.v130),
             str(self.v131), str(self.v132), str(self.v133), str(self.v134), str(self.v135), str(self.v136),
             str(self.v137), str(self.v138), str(self.v139), str(self.v140), str(self.v141), str(self.v142),
             str(self.v143), str(self.v144), str(self.v145), str(self.v146), str(self.v147), str(self.v148),
             str(self.v149), str(self.v150), str(self.v151), str(self.v152), str(self.v153), str(self.v154),
             str(self.v155), str(self.v156), str(self.v157), str(self.v158), str(self.v159), str(self.v160),
             str(self.v161), str(self.v162), str(self.v163), str(self.v164), str(self.v165), str(self.v166),
             str(self.v167), str(self.v168), str(self.v169), str(self.v170), str(self.v171), str(self.v172),
             str(self.v173), str(self.v174), str(self.v175), str(self.v176), str(self.v177), str(self.v178),
             str(self.v179), str(self.v180), str(self.v181), str(self.v182), str(self.v183), str(self.v184),
             str(self.v185), str(self.v186), str(self.v187), str(self.v188), str(self.v189), str(self.v190),
             str(self.v191), str(self.v192), str(self.v193), str(self.v194), str(self.v195), str(self.v196),
             str(self.v197), str(self.v198), str(self.v199), str(self.v200), str(self.v201), str(self.v202),
             str(self.v203), str(self.v204), str(self.v205), str(self.v206), str(self.v207), str(self.v208),
             str(self.v209), str(self.v210), str(self.v211), str(self.v212), str(self.v213), str(self.v214),
             str(self.v215), str(self.v216), str(self.v217), str(self.v218), str(self.v219), str(self.v220),
             str(self.v221), str(self.v222), str(self.v223), str(self.v224), str(self.v225), str(self.v226),
             str(self.v227), str(self.v228), str(self.v229), str(self.v230), str(self.v231), str(self.v232),
             str(self.v233), str(self.v234), str(self.v235), str(self.v236), str(self.v237), str(self.v238),
             str(self.v239), str(self.v240), str(self.v241), str(self.v242), str(self.v243), str(self.v244),
             str(self.v245), str(self.v246), str(self.v247), str(self.v248), str(self.v249), str(self.v250),
             str(self.v251), str(self.v252), str(self.v253), str(self.v254), str(self.v255), str(self.v256),
             str(self.v257), str(self.v258), str(self.v259), str(self.v260), str(self.v261), str(self.v262),
             str(self.v263), str(self.v264), str(self.v265), str(self.v266), str(self.v267), str(self.v268),
             str(self.v269), str(self.v270), str(self.v271), str(self.v272), str(self.v273), str(self.v274),
             str(self.v275), str(self.v276), str(self.v277), str(self.v278), str(self.v279), str(self.v280),
             str(self.v281), str(self.v282), str(self.v283), str(self.v284), str(self.v285), str(self.v286),
             str(self.v287), str(self.v288), str(self.v289), str(self.v290), str(self.v291), str(self.v292),
             str(self.v293), str(self.v294), str(self.v295), str(self.v296), str(self.v297), str(self.v298),
             str(self.v299), str(self.v300)]) + ")>"


if __name__ == "__main__":
    check_database()
    posts = {"Lay's": [
        {'id': 50218, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1489508667, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#улыбкаLays \n\nУлыбаться, улыбаться и еще раз улыбаться - вот наш план на ближайшие 3 месяца! Акция «Собери миллион улыбок» шагает по России! Это национальная кампания, в которой разыгрывается 3 000 000 призов! Подробные правила можно прочесть тут: http://bit.ly/2mRGVUJ. \n\nВы можете выиграть гарантированные призы, сертификаты на увлекательные путешествия, а так же 1 миллион рублей, розыгрыш которого состоится 31 мая! \n\n1. Купите пачку Lay’s с улыбкой :) Улыбнитесь от осознания того, что она у вас в руках! \n2. Откройте пачку, найдите уникальный 10-значный код, находящийся внутри упаковки, и зарегистрируйтесь на www.laysmillion.ru. \n3. Не переставайте улыбаться, ведь чем больше улыбок, тем больше счастливых людей на Земле! Улыбайтесь и выигрывайте призы! Счетчик уже стартовал!',
         'is_pinned': 1, 'attachments': [{'type': 'photo',
                                          'photo': {'id': 456239339, 'album_id': -7, 'owner_id': -39834333,
                                                    'user_id': 100,
                                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2b7d6/o8DymEccQ9c.jpg',
                                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2b7d7/sb_9xmZbPaQ.jpg',
                                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2b7d8/OhKDvvOzb0Y.jpg',
                                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2b7d9/8h2TN4r20GY.jpg',
                                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2b7da/Orp4_wUo38c.jpg',
                                                    'width': 1000, 'height': 700, 'text': '',
                                                    'date': 1489508435, 'post_id': 50218,
                                                    'access_key': '8cee00debfb4abf8c6'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 279, 'can_post': 1},
         'likes': {'count': 6663, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 33, 'user_reposted': 0}},
        {'id': 50790, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1490781615, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#улыбкаLays \n \nСобери миллион улыбок вместе с Lay’s! Покупай, регистрируй и выигрывай! \nПодробности акции: https://vk.cc/6pTHSU',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239347, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2b9dc/8luejbMtiSU.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2b9dd/5qYa_-viI0U.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2b9de/j3QHh3leG74.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2b9df/8Tk8-5z0V58.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2b9e0/Y5nWnz9rCGo.jpg',
                                    'width': 900, 'height': 900, 'text': '', 'date': 1489583660,
                                    'post_id': 50790, 'access_key': 'f9c6b24de663f6dbef'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 11, 'can_post': 1},
         'likes': {'count': 25, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 4, 'user_reposted': 0}},
        {'id': 50740, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1490713753, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "Lay's дарит повод для миллиона улыбок! Регистрируй промокоды на сайте https://vk.cc/6qD7TK и выигрывай крутые призы! Главный приз - 1 000 000 рублей! \n\n#улыбкаLays",
         'attachments': [{'type': 'video', 'video': {'id': 456239082, 'owner_id': -39834333,
                                                     'title': 'Собери миллион улыбок!', 'duration': 15,
                                                     'description': '', 'date': 1490713402, 'comments': 0,
                                                     'views': 5252, 'width': 1920, 'height': 1080,
                                                     'photo_130': 'https://pp.userapi.com/c639530/v639530333/10e1d/yG3Ajl8-PCo.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c639530/v639530333/10e1b/fImx6akg7y8.jpg',
                                                     'photo_800': 'https://pp.userapi.com/c639530/v639530333/10e1a/T88ZEJzm7H8.jpg',
                                                     'access_key': '36de1bb131709a8d79',
                                                     'first_frame_320': 'https://pp.userapi.com/c837122/v837122333/2df1c/lvub4fUjQEQ.jpg',
                                                     'first_frame_160': 'https://pp.userapi.com/c837122/v837122333/2df1d/Q0uY0IvKiTc.jpg',
                                                     'first_frame_130': 'https://pp.userapi.com/c837122/v837122333/2df1e/KlnTvoHePkI.jpg',
                                                     'first_frame_800': 'https://pp.userapi.com/c837122/v837122333/2df1b/0K2x7Bxc3T4.jpg',
                                                     'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 11, 'can_post': 1},
         'likes': {'count': 25, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 50588, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1490432447, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#улыбкаLays \n\nХотите поучаствовать в добром деле?! Lay’s передаст 5000 уроков для воспитанников детских домов, а вы можете помочь удвоить эту цифру! Все просто: сделайте селфи с пачкой Lay’s и выложите в социальные сети с хештегом #улыбкаLays или воспользуйтесь нашим фоторедактором (https://vk.cc/6p2E5g)! Если в галерее мы наберем 1 000 000 фотографий, Lay’s удвоит пожертвование. Подробности о благотворительной акции можно прочесть тут: https://vk.cc/6p2EYb. Больше улыбок - больше добрых дел!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239346, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2b9cf/Se06Xs3yKH8.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2b9d0/ik8WjmcvWhQ.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2b9d1/JWc9TuOfMpg.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2b9d2/t9f1tsP1yvY.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2b9d3/4AdWo24jXQg.jpg',
                                    'width': 900, 'height': 900, 'text': '', 'date': 1489582535,
                                    'post_id': 50588, 'access_key': 'ab0d6214c12366ea6e'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 19, 'can_post': 1},
         'likes': {'count': 130, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 4, 'user_reposted': 0}},
        {'id': 50556, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1490365926, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays\n\nУ меня не бывает такого, чтобы #меняневзяли. А за последний хрустящий ломтик в пачке вообще конкуренция!',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 443632418, 'owner_id': 66569038, 'title': 'меня_не_взяли.gif',
                                  'size': 2975538, 'ext': 'gif',
                                  'url': 'https://vk.com/doc66569038_443632418?hash=3eba10a12de36d443a&dl=149081290621414af6c4fb1c1ee0&api=1&no_preview=1',
                                  'date': 1490359515, 'type': 3, 'preview': {'photo': {'sizes': [
                                  {'src': 'https://pp.userapi.com/c810231/u66569038/-3/m_9bf90f9328.jpg',
                                   'width': 130, 'height': 100, 'type': 'm'},
                                  {'src': 'https://pp.userapi.com/c810231/u66569038/-3/s_9bf90f9328.jpg',
                                   'width': 100, 'height': 75, 'type': 's'},
                                  {'src': 'https://pp.userapi.com/c810231/u66569038/-3/x_9bf90f9328.jpg',
                                   'width': 604, 'height': 604, 'type': 'x'},
                                  {'src': 'https://pp.userapi.com/c810231/u66569038/-3/y_9bf90f9328.jpg',
                                   'width': 807, 'height': 807, 'type': 'y'},
                                  {'src': 'https://pp.userapi.com/c810231/u66569038/-3/o_9bf90f9328.jpg',
                                   'width': 600, 'height': 600, 'type': 'o'}]}, 'video': {
                                  'src': 'https://vk.com/doc66569038_443632418?hash=3eba10a12de36d443a&dl=149081290621414af6c4fb1c1ee0&api=1&mp4=1',
                                  'width': 600, 'height': 600, 'file_size': 103813}},
                                  'access_key': '6a1e3313cbbb55c6c1'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 26, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 50543, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1490357718, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #улыбкаLays\n \nНастало время решить этот вопрос раз и навсегда. Как есть чипсы Lay’s вкуснее: из пачки или из миски?',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239393, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c626421/v626421038/5e706/up8kF6ln53E.jpg',
                                    'photo_130': 'https://pp.userapi.com/c626421/v626421038/5e707/rWHvJwOLGrI.jpg',
                                    'photo_604': 'https://pp.userapi.com/c626421/v626421038/5e708/cIeCwdp-Zx4.jpg',
                                    'photo_807': 'https://pp.userapi.com/c626421/v626421038/5e709/B5b-AEEw4bw.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c626421/v626421038/5e70a/kdqrNWj0P5I.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1490356292,
                                    'access_key': '5f0abf54a2e874ae0d'}}, {'type': 'poll',
                                                                           'poll': {'id': 259662750,
                                                                                    'owner_id': -39834333,
                                                                                    'created': 1490356292,
                                                                                    'question': 'А как это делаете вы?',
                                                                                    'votes': 3673,
                                                                                    'answer_id': 0,
                                                                                    'answers': [
                                                                                        {'id': 869915231,
                                                                                         'text': '- Из миски',
                                                                                         'votes': 875,
                                                                                         'rate': 23.82},
                                                                                        {'id': 869915232,
                                                                                         'text': '- Из пачки',
                                                                                         'votes': 2798,
                                                                                         'rate': 76.18}],
                                                                                    'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 16, 'can_post': 1},
         'likes': {'count': 46, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 3, 'user_reposted': 0}},
        {'id': 50493, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1490270438, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nМир может спать спокойно. Могучие рейнджеры возвращаются! Ни один инопланетный монстр не пройдет, ведь есть пятеро смельчаков, которые обрели суперсилу и должны возродить древний боевой орден. \nКстати, фанаты героев давно спорят — кто из рейнджеров круче? У нас тоже есть такая проблема: какой вкус Lay’s самый-самый?',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239345, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2b9c6/55xSntbLoEY.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2b9c7/89Eohl6JT2w.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2b9c8/cqsDJSYKWE8.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2b9c9/I4S22uc7v-g.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2b9ca/2XQiGb_xkxo.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1489582397,
                                    'access_key': '25845a47c8974cdc97'}}, {'type': 'poll',
                                                                           'poll': {'id': 258684532,
                                                                                    'owner_id': -39834333,
                                                                                    'created': 1489582397,
                                                                                    'question': 'Какой ваш выбор?',
                                                                                    'votes': 923,
                                                                                    'answer_id': 0,
                                                                                    'answers': [
                                                                                        {'id': 866493002,
                                                                                         'text': 'С сыром',
                                                                                         'votes': 132,
                                                                                         'rate': 14.3},
                                                                                        {'id': 866493003,
                                                                                         'text': 'Со сметаной и луком',
                                                                                         'votes': 153,
                                                                                         'rate': 16.58},
                                                                                        {'id': 866493004,
                                                                                         'text': 'С беконом',
                                                                                         'votes': 147,
                                                                                         'rate': 15.93},
                                                                                        {'id': 866493005,
                                                                                         'text': 'С крабом',
                                                                                         'votes': 372,
                                                                                         'rate': 40.3},
                                                                                        {'id': 866493006,
                                                                                         'text': 'Со сметаной и зеленью',
                                                                                         'votes': 119,
                                                                                         'rate': 12.89}],
                                                                                    'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 34, 'can_post': 1},
         'likes': {'count': 40, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 5, 'user_reposted': 0}},
        {'id': 50453, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1490184048, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#улыбкаLays \n\nГарик уже принял участие в акции #улыбкаLays. Теперь ваша очередь! :) Выкладывайте свои фотографии с пачкой Lay's с улыбкой c хэштегом #улыбкаLays!",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239344, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2b9bd/gwV5zonzDgE.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2b9be/7J2sg60Ybac.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2b9bf/eWPB0LM6K4E.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2b9c0/EOaSTkmFdxE.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2b9c1/2JgBzeJPxcI.jpg',
                                    'width': 900, 'height': 900, 'text': '', 'date': 1489582240,
                                    'post_id': 50453, 'access_key': 'bced508ec982a8e8e4'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 12, 'can_post': 1},
         'likes': {'count': 2484, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 11, 'user_reposted': 0}},
        {'id': 50436, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1490112615, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#рифленыйнонежный \n \nМы личности многогранные, можем быть и ласковыми котиками, и колючими кактусами. А можем быть нежными или рифлеными! Lay's и Гарик Харламов запустили тест, который расскажет вам о себе немного больше. Скорее проходите и узнавайте новые грани себя! Подробнее: http://wavy.lays.ru/test/",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239380, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c626421/v626421038/5e025/ZtYmvPQ37ag.jpg',
                                    'photo_130': 'https://pp.userapi.com/c626421/v626421038/5e026/zmUJ0OctrP4.jpg',
                                    'photo_604': 'https://pp.userapi.com/c626421/v626421038/5e027/7kFlHFMCJU8.jpg',
                                    'photo_807': 'https://pp.userapi.com/c626421/v626421038/5e028/l83MG6kct-c.jpg',
                                    'width': 653, 'height': 457, 'text': '', 'date': 1490110866,
                                    'post_id': 50436, 'access_key': '487d6d9cc32171260f'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 2, 'can_post': 1},
         'likes': {'count': 27, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 50429, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1490083256, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nГеймеры, сегодня ваш день! Спустя почти 5 лет после официального анонсирования выходит Mass Effect: Andromeda! В центре сюжета уже не капитан Шеппард, а брат и сестра Райдеры, которым нужно найти новый дом для человечества.',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239343, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2b9b4/ZRf_Tync0oM.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2b9b5/hgJZj0g-sGs.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2b9b6/w_7gO0bv7_c.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2b9b7/v7vzAKJMQCc.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2b9b8/K0xP56T8wlw.jpg',
                                    'width': 900, 'height': 900, 'text': '', 'date': 1489582129,
                                    'post_id': 50429, 'access_key': '9a430b6134d76295ec'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 33, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 50390, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1489996811, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \n \nСегодня Международный день счастья! Самое время улыбнуться! Скорее пишите в комментариях, какие Lay's делают вас самым счастливым человеком на свете?",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239342, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2b9aa/Lb3qdFdEYpc.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2b9ab/uok3Ukw95U8.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2b9ac/oJq6P4xAEyY.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2b9ad/CA5MP4Mf0bg.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2b9ae/tlRLKIrlgLA.jpg',
                                    'photo_2560': 'https://pp.userapi.com/c837737/v837737038/2b9af/mjdAzAOUPbk.jpg',
                                    'width': 2160, 'height': 2160, 'text': '', 'date': 1489582026,
                                    'post_id': 50390, 'access_key': '02de8a18b226a7e010'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 21, 'can_post': 1},
         'likes': {'count': 32, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 50304, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1489759249, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#улыбкаLays \n \nНе можете найти повод для радости в преддверии выходных? Порадуйте себя пачкой Lay's Smile — отпразднуйте день рождения Германа Лэя! В 1932 году он изобрел чипсы, без которых сегодня мы просто не представляем жизнь!",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239351, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2ba06/Kj9_W1IL2ME.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2ba07/wu1W3C84jg8.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2ba08/dZ8OetaDxLQ.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2ba09/Sxej-ImrX7w.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2ba0a/vrfosk7_PPA.jpg',
                                    'width': 960, 'height': 960, 'text': '', 'date': 1489588315,
                                    'post_id': 50304, 'access_key': '5d4757a396e36e2ae7'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 17, 'can_post': 1},
         'likes': {'count': 41, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 50284, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1489740355, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nМы подвели итоги конкурса «Поздравления с 8 марта»! \nПобедителями становятся - барабанная дробь - [id156640234|Albeert Albeert] и [id22175986|Виктория Борисова]! \n \nМы поздравляем наших победителей и благодарим всех за участие! Будьте активнее, впереди вас ждет еще немало интересных конкурсов и море крутых призов!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239359, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c626421/v626421038/5ae9c/Ic3TctTMe78.jpg',
                                    'photo_130': 'https://pp.userapi.com/c626421/v626421038/5ae9d/7Hw2Bo09r2Q.jpg',
                                    'photo_604': 'https://pp.userapi.com/c626421/v626421038/5ae9e/UPPqoy3fDbc.jpg',
                                    'photo_807': 'https://pp.userapi.com/c626421/v626421038/5ae9f/VpQoCMRyAyg.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c626421/v626421038/5aea0/5L7wZeQlqS4.jpg',
                                    'width': 842, 'height': 842, 'text': '', 'date': 1489740147,
                                    'post_id': 50284, 'access_key': '94353b3ad5dc0fa663'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 6, 'can_post': 1},
         'likes': {'count': 32, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 4, 'user_reposted': 0}},
        {'id': 50280, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1489737695, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \n \nВ Ирландии, где сегодня отмечают день Святого Патрика, готовят боксти — традиционные оладьи из картошки с беконом. Нам, чтобы почувствовать причастность к празднику, необязательно искать ирландский ресторан. Достаточно открыть Lay's с беконом!",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239341, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2b9a1/PhNci2s5t9I.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2b9a2/ocVWH17tG-A.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2b9a3/sL1THtfgA3s.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2b9a4/zE5x3R-abd0.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2b9a5/aczHeQlstHs.jpg',
                                    'width': 900, 'height': 900, 'text': '', 'date': 1489581798,
                                    'post_id': 50280, 'access_key': '00fce024874fe7aef0'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 4, 'can_post': 1},
         'likes': {'count': 6376, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 20, 'user_reposted': 0}},
        {'id': 50269, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1489680144, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#рифленыйнонежный \n\nВсе еще не можете отойти от “Логана”? Мы тоже! \nКак вы помните, в фильме появилось только три персонажа из предыдущих фильмов о приключениях Людей Икс. Это сам Росомаха, Чарльз Ксавьер и Калибан. Но помните ли вы остальных? Ищите других персонажей этой вселенной в нашем филворде, а свои ответы оставляйте в комментариях!',
         'attachments': [{'type': 'doc', 'doc': {'id': 443342746, 'owner_id': 66569038,
                                                 'title': 'ezgif.com-video-to-gif (2).gif', 'size': 358039,
                                                 'ext': 'gif',
                                                 'url': 'https://vk.com/doc66569038_443342746?hash=0545a93c6ae8cdf885&dl=1490812907ca5dce9ba30725b5d2&api=1&no_preview=1',
                                                 'date': 1489590136, 'type': 3, 'preview': {'photo': {
                 'sizes': [
                     {'src': 'https://pp.userapi.com/c812337/u66569038/-3/m_4b4a25ba7c.jpg', 'width': 130,
                      'height': 91, 'type': 'm'},
                     {'src': 'https://pp.userapi.com/c812337/u66569038/-3/s_4b4a25ba7c.jpg', 'width': 100,
                      'height': 70, 'type': 's'},
                     {'src': 'https://pp.userapi.com/c812337/u66569038/-3/x_4b4a25ba7c.jpg', 'width': 604,
                      'height': 423, 'type': 'x'},
                     {'src': 'https://pp.userapi.com/c812337/u66569038/-3/y_4b4a25ba7c.jpg', 'width': 807,
                      'height': 565, 'type': 'y'},
                     {'src': 'https://pp.userapi.com/c812337/u66569038/-3/o_4b4a25ba7c.jpg', 'width': 600,
                      'height': 420, 'type': 'o'}]}, 'video': {
                 'src': 'https://vk.com/doc66569038_443342746?hash=0545a93c6ae8cdf885&dl=1490812907ca5dce9ba30725b5d2&api=1&mp4=1',
                 'width': 600, 'height': 420, 'file_size': 76491}}, 'access_key': '573009d654fa1ec3cb'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 6, 'can_post': 1},
         'likes': {'count': 16, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 50260, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1489665745, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \n \nЗавтра выходит первый сезон «Железного кулака». Да-да, сразу все 13 серий! Теперь вам точно будет чем заняться на выходных. Устраивайте киноуикенд, зовите друзей и не забудьте о Lay’s STAX. А чтобы скрасить ожидание, попробуйте посчитать количество туб Lay's Stax. Результаты оставляйте в комментариях!",
         'attachments': [{'type': 'doc', 'doc': {'id': 443338299, 'owner_id': 66569038,
                                                 'title': 'ezgif.com-video-to-gif.gif', 'size': 1005324,
                                                 'ext': 'gif',
                                                 'url': 'https://vk.com/doc66569038_443338299?hash=2199206e8266e8d467&dl=149081290726bab3a65222b7a2bf&api=1&no_preview=1',
                                                 'date': 1489581489, 'type': 3, 'preview': {'photo': {
                 'sizes': [
                     {'src': 'https://pp.userapi.com/c810420/u66569038/-3/m_661b212f81.jpg', 'width': 130,
                      'height': 100, 'type': 'm'},
                     {'src': 'https://pp.userapi.com/c810420/u66569038/-3/s_661b212f81.jpg', 'width': 100,
                      'height': 75, 'type': 's'},
                     {'src': 'https://pp.userapi.com/c810420/u66569038/-3/x_661b212f81.jpg', 'width': 604,
                      'height': 604, 'type': 'x'},
                     {'src': 'https://pp.userapi.com/c810420/u66569038/-3/y_661b212f81.jpg', 'width': 807,
                      'height': 807, 'type': 'y'},
                     {'src': 'https://pp.userapi.com/c810420/u66569038/-3/o_661b212f81.jpg', 'width': 600,
                      'height': 600, 'type': 'o'}]}, 'video': {
                 'src': 'https://vk.com/doc66569038_443338299?hash=2199206e8266e8d467&dl=149081290726bab3a65222b7a2bf&api=1&mp4=1',
                 'width': 600, 'height': 600, 'file_size': 185720}}, 'access_key': 'dd0cce8030cdbeef3f'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 41, 'can_post': 1},
         'likes': {'count': 14009, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 47, 'user_reposted': 0}},
        {'id': 50238, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1489590380, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#рифленыйнонежный \n\nПрошлый четверг стал особенным днём для всех поклонников Кинг-Конга: на экраны вышел десятый фильм про гигантскую обезьяну, «Конг: Остров черепа»! \nВпервые монстр появился в кино 84 года назад и до сих пор не дает покоя кинематографистам. На этот раз борются с чудовищем обладательница «Оскара» Бри Ларсон и Том «Локи» Хиддлстон.\n Еще не посмотрели фильм? Срочно в кино! А пока бронируете билеты, решайте, с каким вкусом рифленых Lay’s отправитесь на Остров Черепа!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239350, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/2b9fd/ILpdi2N5164.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/2b9fe/sXrUwbXDP0o.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/2b9ff/kxnIpYOJv-U.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/2ba00/k-GkY820F04.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/2ba01/QfRNbm9j6PE.jpg',
                                    'width': 900, 'height': 900, 'text': '', 'date': 1489588078,
                                    'access_key': '74d822e22b78f22c02'}}, {'type': 'poll',
                                                                           'poll': {'id': 258695792,
                                                                                    'owner_id': -39834333,
                                                                                    'created': 1489588078,
                                                                                    'question': 'А какой вкус прихватите с собой вы?',
                                                                                    'votes': 435,
                                                                                    'answer_id': 0,
                                                                                    'answers': [
                                                                                        {'id': 866532293,
                                                                                         'text': '«Лобстер»',
                                                                                         'votes': 214,
                                                                                         'rate': 49.2},
                                                                                        {'id': 866532294,
                                                                                         'text': '«Нежный сыр с луком»',
                                                                                         'votes': 221,
                                                                                         'rate': 50.8}],
                                                                                    'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 1, 'can_post': 1},
         'likes': {'count': 15, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 50157, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1489062543, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#рифленыйнонежный \n\nКонкурс от Lay’s и блогеров! \n \nНа официальном сайте Lay’s (http://wavy.lays.ru/constructor/) создайте свою рифленую стерео фотографию. \nДелитесь ею с друзьями в социальных сетях, не забывая использовать хэштег #рифленыйнонежный. \nКаждые две недели наше жюри, состоящее из известных блогеров, будет выбирать лучшие работы в пяти номинациях! \nВ номинации «За самое брутальное стереофото» определять победителей будет Андрей Глазунов (https://www.instagram.com/agvlog/). \nЕго стерео фото вы можете найти в нашем посте ;)\n\nНе упустите возможность получить крутые призы от Lay's!",
         'attachments': [{'type': 'doc',
                          'doc': {'id': 443125062, 'owner_id': 66569038, 'title': 'gif_bloger_1_1.gif',
                                  'size': 439960, 'ext': 'gif',
                                  'url': 'https://vk.com/doc66569038_443125062?hash=0e4314c4fc884ac127&dl=1490812907ed0a6c47dcde898e5f&api=1&no_preview=1',
                                  'date': 1488886489, 'type': 3, 'preview': {'photo': {'sizes': [{
                                  'src': 'https://cs7065.userapi.com/c810623/u66569038/-3/m_e30f734696.jpg',
                                  'width': 130,
                                  'height': 100,
                                  'type': 'm'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c810623/u66569038/-3/s_e30f734696.jpg',
                                      'width': 100,
                                      'height': 75,
                                      'type': 's'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c810623/u66569038/-3/x_e30f734696.jpg',
                                      'width': 604,
                                      'height': 604,
                                      'type': 'x'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c810623/u66569038/-3/y_e30f734696.jpg',
                                      'width': 807,
                                      'height': 807,
                                      'type': 'y'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c810623/u66569038/-3/o_e30f734696.jpg',
                                      'width': 800,
                                      'height': 800,
                                      'type': 'o'}]},
                                  'video': {
                                      'src': 'https://vk.com/doc66569038_443125062?hash=0e4314c4fc884ac127&dl=1490812907ed0a6c47dcde898e5f&api=1&mp4=1',
                                      'width': 800,
                                      'height': 800,
                                      'file_size': 187386}},
                                  'access_key': '98d049f8b3dfebb35b'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 7, 'can_post': 1},
         'likes': {'count': 31, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 50138, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488979839, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nВсех девушек поздравляем с 8 Марта! Всегда оставайтесь собой и никогда не унывайте! Вокруг целый мир, который вы наверняка сможете покорить! А начать можно прямо сейчас!',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 443155472, 'owner_id': 66569038, 'title': 'Праздник!.gif',
                                  'size': 491022, 'ext': 'gif',
                                  'url': 'https://vk.com/doc66569038_443155472?hash=32a776c8e1119ed2a9&dl=14908129070ef5f2d0735901ac10&api=1&no_preview=1',
                                  'date': 1488962891, 'type': 3, 'preview': {'photo': {'sizes': [
                                  {'src': 'https://pp.userapi.com/c810233/u66569038/-3/m_0e299d2ae6.jpg',
                                   'width': 130, 'height': 100, 'type': 'm'},
                                  {'src': 'https://pp.userapi.com/c810233/u66569038/-3/s_0e299d2ae6.jpg',
                                   'width': 100, 'height': 75, 'type': 's'},
                                  {'src': 'https://pp.userapi.com/c810233/u66569038/-3/x_0e299d2ae6.jpg',
                                   'width': 604, 'height': 604, 'type': 'x'},
                                  {'src': 'https://pp.userapi.com/c810233/u66569038/-3/y_0e299d2ae6.jpg',
                                   'width': 807, 'height': 807, 'type': 'y'},
                                  {'src': 'https://pp.userapi.com/c810233/u66569038/-3/z_0e299d2ae6.jpg',
                                   'width': 1280, 'height': 1280, 'type': 'z'},
                                  {'src': 'https://pp.userapi.com/c810233/u66569038/-3/o_0e299d2ae6.jpg',
                                   'width': 900, 'height': 900, 'type': 'o'}]}, 'video': {
                                  'src': 'https://vk.com/doc66569038_443155472?hash=32a776c8e1119ed2a9&dl=14908129070ef5f2d0735901ac10&api=1&mp4=1',
                                  'width': 900, 'height': 900, 'file_size': 263826}},
                                  'access_key': 'cb77238f279bf7d607'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 7, 'can_post': 1},
         'likes': {'count': 27, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 50129, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488963834, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nНаконец-то весна! Наконец-то праздник! Ярких впечатлений, незабываемых эмоций, море приключений, а Lay’s STAX всегда будет рядом!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239323, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/29a9e/4eLPK2V-EoM.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/29a9f/y0fKZZUozFE.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/29aa0/_yt02tp74aU.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/29aa1/kqMntZgCg1o.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/29aa2/nbPbvNHiWpU.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1488960800,
                                    'post_id': 50129, 'access_key': 'e7568ee3bbdb8cc03a'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 3, 'can_post': 1},
         'likes': {'count': 313, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 3, 'user_reposted': 0}},
        {'id': 50128, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488963830, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nЭто ваша весна, ваш день - 8 марта! Ярких впечатлений, пусть у вас будет действительно вкусная жизнь\u200b, а \u200bLay’s STAX\u200b всегда будет рядом!',
         'attachments': [{'type': 'doc', 'doc': {'id': 443156732, 'owner_id': 66569038,
                                                 'title': 'ezgif.com-video-to-gif.gif', 'size': 1980826,
                                                 'ext': 'gif',
                                                 'url': 'https://vk.com/doc66569038_443156732?hash=38e66a52a5a393f40b&dl=1490812907ac3bffe9d21263027c&api=1&no_preview=1',
                                                 'date': 1488965509, 'type': 3, 'preview': {'photo': {
                 'sizes': [
                     {'src': 'https://pp.userapi.com/c812120/u66569038/-3/m_5deddca9ab.jpg', 'width': 130,
                      'height': 100, 'type': 'm'},
                     {'src': 'https://pp.userapi.com/c812120/u66569038/-3/s_5deddca9ab.jpg', 'width': 100,
                      'height': 75, 'type': 's'},
                     {'src': 'https://pp.userapi.com/c812120/u66569038/-3/x_5deddca9ab.jpg', 'width': 604,
                      'height': 604, 'type': 'x'},
                     {'src': 'https://pp.userapi.com/c812120/u66569038/-3/y_5deddca9ab.jpg', 'width': 807,
                      'height': 807, 'type': 'y'},
                     {'src': 'https://pp.userapi.com/c812120/u66569038/-3/o_5deddca9ab.jpg', 'width': 600,
                      'height': 600, 'type': 'o'}]}, 'video': {
                 'src': 'https://vk.com/doc66569038_443156732?hash=38e66a52a5a393f40b&dl=1490812907ac3bffe9d21263027c&api=1&mp4=1',
                 'width': 600, 'height': 600, 'file_size': 168674}}, 'access_key': 'bd0f796ccf42690717'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 330, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 7, 'user_reposted': 0}},
        {'id': 50124, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488961940, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nС любимым человеком каждая встреча – это праздник, а 8 марта это ощущается ярче всего. Этот день - отличный повод признаться любимым в своих чувствах, а Lay’s STAX\u200b в этом поможет!',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 443154055, 'owner_id': 66569038, 'title': 'present.gif',
                                  'size': 7307218, 'ext': 'gif',
                                  'url': 'https://vk.com/doc66569038_443154055?hash=deed3f5cf96dd40f56&dl=14908129070aa094ccd5a38fefa2&api=1&no_preview=1',
                                  'date': 1488959475, 'type': 3, 'preview': {'photo': {'sizes': [
                                  {'src': 'https://pp.userapi.com/c810529/u66569038/-3/m_49c98c2595.jpg',
                                   'width': 130, 'height': 100, 'type': 'm'},
                                  {'src': 'https://pp.userapi.com/c810529/u66569038/-3/s_49c98c2595.jpg',
                                   'width': 100, 'height': 75, 'type': 's'},
                                  {'src': 'https://pp.userapi.com/c810529/u66569038/-3/x_49c98c2595.jpg',
                                   'width': 604, 'height': 604, 'type': 'x'},
                                  {'src': 'https://pp.userapi.com/c810529/u66569038/-3/y_49c98c2595.jpg',
                                   'width': 807, 'height': 807, 'type': 'y'},
                                  {'src': 'https://pp.userapi.com/c810529/u66569038/-3/o_49c98c2595.jpg',
                                   'width': 600, 'height': 600, 'type': 'o'}]}, 'video': {
                                  'src': 'https://vk.com/doc66569038_443154055?hash=deed3f5cf96dd40f56&dl=14908129070aa094ccd5a38fefa2&api=1&mp4=1',
                                  'width': 600, 'height': 600, 'file_size': 256236}},
                                  'access_key': 'eda733cb2c5bf9c6f5'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 213, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 5, 'user_reposted': 0}},
        {'id': 50120, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488960429, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nЭто ваша весна, ваш день - 8 марта! Желаем \u200bтепла и любви, \u200bвсегда оставаться \u200b\u200bсобой\u200b и\u200b след\u200bовать\u200b за мечтой\u200b, а \u200b Lay’s STAX\u200b \u200bвсегда вам \u200bсоставит компанию!',
         'attachments': [{'type': 'doc', 'doc': {'id': 443156845, 'owner_id': 66569038,
                                                 'title': 'ezgif.com-video-to-gif (1).gif', 'size': 1528818,
                                                 'ext': 'gif',
                                                 'url': 'https://vk.com/doc66569038_443156845?hash=a5d1cdafea178b1d7f&dl=1490812907d5a25685ff10ab9cd4&api=1&no_preview=1',
                                                 'date': 1488965676, 'type': 3, 'preview': {'photo': {
                 'sizes': [
                     {'src': 'https://pp.userapi.com/c810434/u66569038/-3/m_2e098f3ce9.jpg', 'width': 130,
                      'height': 100, 'type': 'm'},
                     {'src': 'https://pp.userapi.com/c810434/u66569038/-3/s_2e098f3ce9.jpg', 'width': 100,
                      'height': 75, 'type': 's'},
                     {'src': 'https://pp.userapi.com/c810434/u66569038/-3/x_2e098f3ce9.jpg', 'width': 604,
                      'height': 604, 'type': 'x'},
                     {'src': 'https://pp.userapi.com/c810434/u66569038/-3/y_2e098f3ce9.jpg', 'width': 807,
                      'height': 807, 'type': 'y'},
                     {'src': 'https://pp.userapi.com/c810434/u66569038/-3/o_2e098f3ce9.jpg', 'width': 600,
                      'height': 600, 'type': 'o'}]}, 'video': {
                 'src': 'https://vk.com/doc66569038_443156845?hash=a5d1cdafea178b1d7f&dl=1490812907d5a25685ff10ab9cd4&api=1&mp4=1',
                 'width': 600, 'height': 600, 'file_size': 313786}}, 'access_key': '75a55324eb1a191759'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 79, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 3, 'user_reposted': 0}},
        {'id': 50105, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488904146, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#рифленыйнонежный \n\nНадеемся, что вы уже успели оценить новые и изысканные вкусы рифленых Lay’s! Если да, то самое время узнать, какой из них понравился вам больше всего: “Нежный сыр и лук” или “Лобстер”?',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239319, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837737/v837737038/298a9/LM36B4D2ENk.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837737/v837737038/298aa/6-ViDkb3v9s.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837737/v837737038/298ab/6QyZ8BmJwsw.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837737/v837737038/298ac/nf6TNWQIeT4.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837737/v837737038/298ad/zf2jBT7qOLY.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1488886259,
                                    'access_key': '4a959f1d20f2bb2bc5'}}, {'type': 'poll',
                                                                           'poll': {'id': 257819566,
                                                                                    'owner_id': -39834333,
                                                                                    'created': 1488886259,
                                                                                    'question': 'Какой вкус вам понравился больше?',
                                                                                    'votes': 424,
                                                                                    'answer_id': 0,
                                                                                    'answers': [
                                                                                        {'id': 863486808,
                                                                                         'text': '“Нежный сыр и лук”',
                                                                                         'votes': 210,
                                                                                         'rate': 49.53},
                                                                                        {'id': 863486809,
                                                                                         'text': '“Лобстер”',
                                                                                         'votes': 214,
                                                                                         'rate': 50.47}],
                                                                                    'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 8, 'can_post': 1},
         'likes': {'count': 22, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 50104, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488902412, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': 'У всех нас много дел и планов, нужно все успеть и быть на высоте… Но нужно помнить, что хороший отдых – залог отличной продуктивности! Устройте себе настоящий релакс-день! Например, как Юля Пушман – проведите уютный день дома с близкими друзьями или посмотрите любимый сериал. Lay’s STAX отлично дополнит любые приятные моменты!',
         'attachments': [{'type': 'video', 'video': {'id': 456239081, 'owner_id': -39834333,
                                                     'title': 'Мой идеальный выходной || Юлия Пушман',
                                                     'duration': 257,
                                                     'description': 'Редкие, но от этого еще более ценные приятные моменты домашнего чиллинга. Мой идеальный выходной. \nДругие советы как сделать приятные моменты идеальными на сайте Lay’s Stax: https://goo.gl/EyVaxx\n\n♔ИНСТАГРАМ: http://instagram.com/pusshman\n♔ВКОНТАКТЕ:  http://vk.com/pushmanjulia\n♔ТВИТТЕР: https://twitter.com/JuliaPushman \n♔PERISCOPE: https://www.periscope.tv/JuliaPushman\n♔ASK.FM: http://ask.fm/JuliaPushman\n\nСотрудничество: pusshman@zagency.ru',
                                                     'date': 1488555731, 'comments': 0, 'views': 184,
                                                     'photo_130': 'https://pp.userapi.com/c836330/u340295070/video/s_877300e3.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c836330/u340295070/video/l_ebb2787b.jpg',
                                                     'photo_800': 'https://pp.userapi.com/c836330/u340295070/video/x_8d46615a.jpg',
                                                     'access_key': 'e798735d2d0a72590e',
                                                     'platform': 'YouTube', 'can_add': 1}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 14, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 50100, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488896120, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nВ преддверии 8 марта мы хотим послушать ваши истории о том, какие приятные моменты ожидают вас в день праздника! \nИ специально для этого объявляем наш новый конкурс. \n \nПринять участие просто: до 8 марта всем мужчинам нужно рассказать в комментариях к посту, как они создадут приятный момент для своих драгоценных женщин в день их праздника. \nА после 8 марта мы ждем рассказов от девушек, какие приятные моменты подарили им их мужчины. \n \n10 марта жюри прочитает все работы и выберет по 1 победителю среди девушек и парней, которым достанутся призы — по 2 электронных билета в кино! \n \nСроки конкурса: \nПрием работ первого этапа (парни) — с 7 по 8 марта включительно. \nПрием работ второго этапа (девушки) — с 8 по 9 марта включительно. \n\nПусть волшебные моменты станут еще приятнее этой весной!',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 443131045, 'owner_id': 66569038, 'title': '8_марта.gif',
                                  'size': 1170597, 'ext': 'gif',
                                  'url': 'https://vk.com/doc66569038_443131045?hash=738b382bf41a82365c&dl=1490812907392828b1105586b5ea&api=1&no_preview=1',
                                  'date': 1488896648, 'type': 3, 'preview': {'photo': {'sizes': [
                                  {'src': 'https://pp.userapi.com/c810328/u66569038/-3/m_8f86f74b38.jpg',
                                   'width': 130, 'height': 100, 'type': 'm'},
                                  {'src': 'https://pp.userapi.com/c810328/u66569038/-3/s_8f86f74b38.jpg',
                                   'width': 100, 'height': 75, 'type': 's'},
                                  {'src': 'https://pp.userapi.com/c810328/u66569038/-3/x_8f86f74b38.jpg',
                                   'width': 604, 'height': 604, 'type': 'x'},
                                  {'src': 'https://pp.userapi.com/c810328/u66569038/-3/y_8f86f74b38.jpg',
                                   'width': 807, 'height': 807, 'type': 'y'},
                                  {'src': 'https://pp.userapi.com/c810328/u66569038/-3/z_8f86f74b38.jpg',
                                   'width': 1280, 'height': 1280, 'type': 'z'},
                                  {'src': 'https://pp.userapi.com/c810328/u66569038/-3/o_8f86f74b38.jpg',
                                   'width': 900, 'height': 900, 'type': 'o'}]}, 'video': {
                                  'src': 'https://vk.com/doc66569038_443131045?hash=738b382bf41a82365c&dl=1490812907392828b1105586b5ea&api=1&mp4=1',
                                  'width': 900, 'height': 900, 'file_size': 382251}},
                                  'access_key': '504e76d5ffd2f52121'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 24, 'can_post': 1},
         'likes': {'count': 46, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 4, 'user_reposted': 0}},
        {'id': 50067, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488738622, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': 'Мастера творчества Трум Трум не понаслышке знают, как иногда бывает сложно поймать вдохновение. Но вместе мы нашли универсального вдохновителя! Lay’s STAX не только делает яркие моменты еще приятнее, но и помогает развить фантазию и креативное мышление. \nСмотрите скорее, как превратить пустую тубу Lay’s STAX в стильный аксессуар или полезный предмет для дома!',
         'attachments': [{'type': 'video', 'video': {'id': 456239079, 'owner_id': -39834333,
                                                     'title': '5 лайфхаков для декора', 'duration': 626,
                                                     'description': 'Заходите на сайт https://goo.gl/tVTcnV там вы сможете найти много интересных советов, как сделать свои любимые моменты приятнее.\nВ нашем новом видео мы покажем пять простых способов как превратить пустые упаковки от чипсов в яркие аксессуары и предметы декора. С Lay`s STAX не только приятно смотреть любимый фильм или играть в настольные игры с друзьями, но и придумывать что-то невероятное. Немного времени и терпения, и удобная туба без особого труда превращается в стильные яркие браслеты, органайзер для раб',
                                                     'date': 1488554680, 'comments': 0, 'views': 6713,
                                                     'photo_130': 'https://pp.userapi.com/c836134/u9198560/video/s_759a95b2.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c836134/u9198560/video/l_f8f27665.jpg',
                                                     'photo_640': 'https://pp.userapi.com/c836134/u9198560/video/y_9ac403d9.jpg',
                                                     'access_key': '961c6407a703cf754c',
                                                     'platform': 'YouTube', 'can_add': 1}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 19, 'can_post': 1},
         'likes': {'count': 20, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 50030, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488558012, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': 'Lay’s STAX профессионалы приятных моментов! Наши друзья - ВJobыватели убедились в этом, ведь Lay’s STAX делают яркие моменты еще приятнее и даже помогают спасать ситуации, выхода из которых, казалось, нет! Заинтригованы? Скорее смотрите!',
         'attachments': [{'type': 'video', 'video': {'id': 456239077, 'owner_id': -39834333,
                                                     'title': 'ОКОЛО ФУТБОЛА / спортивная трансляция / НОВОЕ ШОУ',
                                                     'duration': 388,
                                                     'description': "Собрался насладиться просмотром футбола? Тогда наши советы как сделать приятный момент идеальным будут очень кстати! \nКстати на сайте Lay's Stax: https://goo.gl/ZHPXeN ты найдешь и другие рекомендации от профессионалов приятных моментов. \nСмотри и наслаждайся идеальными приятными моментами.\nПишите в комментариях как вам новое шоу? от 1 до 5!\nНаш INSTAGRAM http://instagram.com/VJOBIVAY\nПаблик ВКонтакте - https://vk.com/vjobivay\n\nКанал Антона из Франции: https://www.youtube.com/user/antonizfrantsii\nINSTAGRAM",
                                                     'date': 1488554511, 'comments': 0, 'views': 1261,
                                                     'photo_130': 'https://pp.userapi.com/c837532/u89626/video/s_8fc25eb9.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c837532/u89626/video/l_c943e8f2.jpg',
                                                     'photo_640': 'https://pp.userapi.com/c837532/u89626/video/y_42be2056.jpg',
                                                     'access_key': 'f9ce907d0feadc4953',
                                                     'platform': 'YouTube', 'can_add': 1}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 18, 'can_post': 1},
         'likes': {'count': 17, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49957, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488105121, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nЗавтра весь мир будет отмечать День оптимиста. Сегодня самое время решить этот вопрос раз и навсегда: пачка наполовину пуста или наполовину полна?',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239248, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837736/v837736038/2541d/HYNo3e6ieuE.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837736/v837736038/2541e/8KpNFbnZawE.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837736/v837736038/2541f/Aasz5mLWJrY.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837736/v837736038/25420/OfN_dxLA93k.jpg',
                                    'width': 800, 'height': 800, 'text': '', 'date': 1487340414,
                                    'access_key': '953ffb57ae6b32f2ef'}}, {'type': 'poll',
                                                                           'poll': {'id': 255752581,
                                                                                    'owner_id': -39834333,
                                                                                    'created': 1487340414,
                                                                                    'question': 'Как вы считаете?',
                                                                                    'votes': 830,
                                                                                    'answer_id': 0,
                                                                                    'answers': [
                                                                                        {'id': 856292396,
                                                                                         'text': 'Пачка наполовину пуста',
                                                                                         'votes': 498,
                                                                                         'rate': 60.0},
                                                                                        {'id': 856292397,
                                                                                         'text': 'Пачка наполовину полна',
                                                                                         'votes': 332,
                                                                                         'rate': 40.0}],
                                                                                    'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 30, 'can_post': 1},
         'likes': {'count': 40, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 5, 'user_reposted': 0}},
        {'id': 49945, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1488018742, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong \n \nСегодня суббота – самое время встретиться с друзьями! Главное – не забыть запастись чипсами. Предлагаем вам набрать необходимое количество Lay’s, чтобы сравнять весы! Включайте видео, ставьте на паузу в правильное время и выкладывайте скриншот в комментарии!',
         'attachments': [{'type': 'video',
                          'video': {'id': 456239074, 'owner_id': -39834333, 'title': 'Weekend',
                                    'duration': 1, 'description': '', 'date': 1487753135, 'comments': 0,
                                    'views': 6022, 'width': 800, 'height': 800,
                                    'photo_130': 'https://pp.userapi.com/c639718/v639718333/920a/_NTQV2rkD_E.jpg',
                                    'photo_320': 'https://pp.userapi.com/c639718/v639718333/9208/ImtHltdo8fk.jpg',
                                    'photo_800': 'https://pp.userapi.com/c639718/v639718333/9207/MalaFanSs9o.jpg',
                                    'access_key': '58575be4b96a55ef21', 'repeat': 1,
                                    'first_frame_320': 'https://pp.userapi.com/c639526/v639526333/99cd/pk-Mfmpk1zs.jpg',
                                    'first_frame_160': 'https://pp.userapi.com/c639526/v639526333/99ce/oi-oYM3HleY.jpg',
                                    'first_frame_130': 'https://pp.userapi.com/c639526/v639526333/99cf/Tnhl-QDlnvg.jpg',
                                    'first_frame_800': 'https://pp.userapi.com/c639526/v639526333/99cc/jyOublI1nxc.jpg',
                                    'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 9, 'can_post': 1},
         'likes': {'count': 25, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49922, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487842336, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong \n\nСегодня выходит в прокат наш\u200b \u200b «ответ» многочисленным зарубежным фильмам о супергероях\u200b! \u200bИз фильма «Защитники» мы узнаем, что российские супергерои призваны защищать тех, «кто даже не подозревает об их существовании»! Запасай\u200bтесь\u200b Lay’s\u200b \u200bи \u200bне \u200bзабудь\u200bте про \u200bто, что в кино лучше ходить в\u200b компании лучших друзей!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239247, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837736/v837736038/25415/foG1EjnIxeY.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837736/v837736038/25416/z619LG_x4Do.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837736/v837736038/25417/oyOWCmes73Y.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837736/v837736038/25418/SBGGkzf5cg0.jpg',
                                    'width': 800, 'height': 800, 'text': '', 'date': 1487340335,
                                    'access_key': '59d2dd0ffb261f5759'}}, {'type': 'poll',
                                                                           'poll': {'id': 255752432,
                                                                                    'owner_id': -39834333,
                                                                                    'created': 1487340335,
                                                                                    'question': 'Кто из\u200b супер-геро\u200bев вам ближе?\u200b',
                                                                                    'votes': 354,
                                                                                    'answer_id': 0,
                                                                                    'answers': [
                                                                                        {'id': 856291787,
                                                                                         'text': 'Арсус (человек-зверь, богатырь из Сибири)',
                                                                                         'votes': 127,
                                                                                         'rate': 35.88},
                                                                                        {'id': 856291788,
                                                                                         'text': 'Хан (человек-ветер, владеющий всеми видами восточных единоборств)',
                                                                                         'votes': 83,
                                                                                         'rate': 23.45},
                                                                                        {'id': 856291789,
                                                                                         'text': 'Лер (человек-земля, способный управлять камнями и почвами)',
                                                                                         'votes': 27,
                                                                                         'rate': 7.63},
                                                                                        {'id': 856291790,
                                                                                         'text': 'Ксения (человек-вода, обладающая гибкостью и выносливостью)',
                                                                                         'votes': 117,
                                                                                         'rate': 33.05}],
                                                                                    'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 8, 'can_post': 1},
         'likes': {'count': 24, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49905, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487770268, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nВозьмет ли Энрике Оскар за участие в нашем ролике? Не важно! \nВажно, что Энрике предлагает вам запастись новинкой от Lay’s при просмотре церемонии. \n\nВедь с новыми Lay’s STAX приятные моменты станут еще приятнее! \n\nПодробнее: https://vk.cc/6hfj0i',
         'attachments': [{'type': 'video',
                          'video': {'id': 456239075, 'owner_id': -39834333, 'title': "Lay's STAX",
                                    'duration': 15, 'description': '', 'date': 1487769658, 'comments': 160,
                                    'views': 23112715, 'width': 1920, 'height': 1080,
                                    'photo_130': 'https://pp.userapi.com/c837732/v837732333/24fe2/9_Q4ktBb5io.jpg',
                                    'photo_320': 'https://pp.userapi.com/c837732/v837732333/24fe0/6sTKB1nReKw.jpg',
                                    'photo_800': 'https://pp.userapi.com/c837732/v837732333/24fdf/dENOgn5pD6s.jpg',
                                    'access_key': '9824f614cd00b58875', 'repeat': 1,
                                    'first_frame_320': 'https://pp.userapi.com/c638825/v638825333/29469/ZgC8qz--T8E.jpg',
                                    'first_frame_160': 'https://pp.userapi.com/c638825/v638825333/2946a/fgX_gpH2drU.jpg',
                                    'first_frame_130': 'https://pp.userapi.com/c638825/v638825333/2946b/bCPjj16ojRc.jpg',
                                    'first_frame_800': 'https://pp.userapi.com/c638825/v638825333/29468/WmddZdjDmlA.jpg',
                                    'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 16, 'can_post': 1},
         'likes': {'count': 11298, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 217, 'user_reposted': 0}},
        {'id': 49891, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487752342, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nВесна близко! Впереди целых четыре дня выходных – самое время успеть наверстать упущенное за зиму! Предлагаем вам разгадать наш филлворд с тематикой «Выходные». Свои ответы выкладывайте в комментарии!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239246, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837736/v837736038/25408/FkPUEhJLA2U.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837736/v837736038/25409/IEBAL39ZEBM.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837736/v837736038/2540a/B2QHpD6ZpBE.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837736/v837736038/2540b/ic6ZQwO-rVM.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837736/v837736038/2540c/r21_j4-erWc.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1487340247,
                                    'post_id': 49891, 'access_key': '5d1222b8e40c72a217'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 26, 'can_post': 1},
         'likes': {'count': 23, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49886, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487681281, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#футболвкуснеесLays \n\nСегодня в 22:45 (МСК) начнется матч группового этапа Лиги Чемпионов УЕФА «Манчестер Сити» – «Монако»! Французы играют с родоначальниками футбола - англичанами. \n\nПосмотрим, сможет ли самый дорогой игрок «Монако» ярко проявить себя в Манчестере!',
         'attachments': [{'type': 'doc', 'doc': {'id': 442400424, 'owner_id': 66569038, 'title': '13_2.gif',
                                                 'size': 1973178, 'ext': 'gif',
                                                 'url': 'https://vk.com/doc66569038_442400424?hash=8534d3f28acdb02259&dl=1490812907070a4ab467bba9f332&api=1&no_preview=1',
                                                 'date': 1487340054, 'type': 3, 'preview': {'photo': {
                 'sizes': [
                     {'src': 'https://pp.userapi.com/c812723/u66569038/-3/m_48471319ea.jpg', 'width': 130,
                      'height': 100, 'type': 'm'},
                     {'src': 'https://pp.userapi.com/c812723/u66569038/-3/s_48471319ea.jpg', 'width': 100,
                      'height': 75, 'type': 's'},
                     {'src': 'https://pp.userapi.com/c812723/u66569038/-3/x_48471319ea.jpg', 'width': 604,
                      'height': 604, 'type': 'x'},
                     {'src': 'https://pp.userapi.com/c812723/u66569038/-3/y_48471319ea.jpg', 'width': 807,
                      'height': 807, 'type': 'y'},
                     {'src': 'https://pp.userapi.com/c812723/u66569038/-3/o_48471319ea.jpg', 'width': 800,
                      'height': 800, 'type': 'o'}]}, 'video': {
                 'src': 'https://vk.com/doc66569038_442400424?hash=8534d3f28acdb02259&dl=1490812907070a4ab467bba9f332&api=1&mp4=1',
                 'width': 800, 'height': 800, 'file_size': 752837}}, 'access_key': 'eb3362437b2a2fb055'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 5, 'can_post': 1},
         'likes': {'count': 19, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49885, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487662341, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nФанаты Halo Wars, ликуйте! Релиз второй части культовой игры уже сегодня! А чтобы скрасить ожидание, предлагаем вам ознакомиться с подборкой лучших игр в выбранном жанре.',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 442400521, 'owner_id': 66569038, 'title': '15_1 (1).gif',
                                  'size': 394882, 'ext': 'gif',
                                  'url': 'https://vk.com/doc66569038_442400521?hash=3036f177ab9d59ae37&dl=149081290786907c051f2867a21c&api=1&no_preview=1',
                                  'date': 1487340155, 'type': 3, 'preview': {'photo': {'sizes': [{
                                  'src': 'https://cs7065.userapi.com/c812324/u66569038/-3/m_493e7a0fe6.jpg',
                                  'width': 130,
                                  'height': 100,
                                  'type': 'm'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812324/u66569038/-3/s_493e7a0fe6.jpg',
                                      'width': 100,
                                      'height': 75,
                                      'type': 's'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812324/u66569038/-3/x_493e7a0fe6.jpg',
                                      'width': 604,
                                      'height': 604,
                                      'type': 'x'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812324/u66569038/-3/y_493e7a0fe6.jpg',
                                      'width': 807,
                                      'height': 807,
                                      'type': 'y'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812324/u66569038/-3/o_493e7a0fe6.jpg',
                                      'width': 800,
                                      'height': 800,
                                      'type': 'o'}]},
                                  'video': {
                                      'src': 'https://vk.com/doc66569038_442400521?hash=3036f177ab9d59ae37&dl=149081290786907c051f2867a21c&api=1&mp4=1',
                                      'width': 800,
                                      'height': 800,
                                      'file_size': 115072}},
                                  'access_key': 'a6d1563e18582a3a6e'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 20, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49881, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487576881, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nВо Всемирный день справедливости не жадничай - поделись чипсами Lay’s с другими хотя бы сегодня!',
         'attachments': [{'type': 'doc', 'doc': {'id': 442403755, 'owner_id': 66569038, 'title': '17_1.gif',
                                                 'size': 777413, 'ext': 'gif',
                                                 'url': 'https://vk.com/doc66569038_442403755?hash=9461b2e4d02e9457f6&dl=14908129079f321a23c546f13282&api=1&no_preview=1',
                                                 'date': 1487344018, 'type': 3, 'preview': {'photo': {
                 'sizes': [
                     {'src': 'https://pp.userapi.com/c810228/u66569038/-3/m_e079265b8a.jpg', 'width': 130,
                      'height': 100, 'type': 'm'},
                     {'src': 'https://pp.userapi.com/c810228/u66569038/-3/s_e079265b8a.jpg', 'width': 100,
                      'height': 75, 'type': 's'},
                     {'src': 'https://pp.userapi.com/c810228/u66569038/-3/x_e079265b8a.jpg', 'width': 604,
                      'height': 604, 'type': 'x'},
                     {'src': 'https://pp.userapi.com/c810228/u66569038/-3/y_e079265b8a.jpg', 'width': 807,
                      'height': 807, 'type': 'y'},
                     {'src': 'https://pp.userapi.com/c810228/u66569038/-3/z_e079265b8a.jpg', 'width': 1280,
                      'height': 1280, 'type': 'z'},
                     {'src': 'https://pp.userapi.com/c810228/u66569038/-3/o_e079265b8a.jpg', 'width': 1000,
                      'height': 1000, 'type': 'o'}]}, 'video': {
                 'src': 'https://vk.com/doc66569038_442403755?hash=9461b2e4d02e9457f6&dl=14908129079f321a23c546f13282&api=1&mp4=1',
                 'width': 1000, 'height': 1000, 'file_size': 242633}},
                                                 'access_key': '806f4ae1f99bd18fe2'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 4, 'can_post': 1},
         'likes': {'count': 24, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49864, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487422083, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nВыходные без Lay’s, как поговаривают, не выходные. Попробуйте поймать удачу в дартс и попасть точно в цель, чтобы выиграть Lay’s со вкусом «С солью»! Все просто - ставь на паузу в нужный момент и результат со скриншотом выкладывай в комментарии!',
         'attachments': [{'type': 'video',
                          'video': {'id': 456239069, 'owner_id': -39834333, 'title': 'Сыграем в дартс!',
                                    'duration': 5, 'description': '', 'date': 1487345695, 'comments': 0,
                                    'views': 2848, 'width': 1920, 'height': 1080,
                                    'photo_130': 'https://pp.userapi.com/c638017/v638017333/3647a/XInmYmwt9hU.jpg',
                                    'photo_320': 'https://pp.userapi.com/c638017/v638017333/36478/dl3el7JRtkA.jpg',
                                    'photo_800': 'https://pp.userapi.com/c638017/v638017333/36477/0mm-YU67U2c.jpg',
                                    'access_key': 'e8df09a07dc87f70e1', 'repeat': 1,
                                    'first_frame_320': 'https://pp.userapi.com/c837233/v837233333/281ea/L7CYGv_osaM.jpg',
                                    'first_frame_160': 'https://pp.userapi.com/c837233/v837233333/281eb/4E7FzINaRx0.jpg',
                                    'first_frame_130': 'https://pp.userapi.com/c837233/v837233333/281ec/nQRIkrMmd70.jpg',
                                    'first_frame_800': 'https://pp.userapi.com/c837233/v837233333/281e9/F5A0hTzM3rQ.jpg',
                                    'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 27, 'can_post': 1},
         'likes': {'count': 16, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49859, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487346488, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#киновкуснеесLays \n \nФинальная часть серии фильмов «Обитель зла» наконец-то в кино! Бросайте все и бегите в кинотеатры, чтобы узнать, чем же закончилась борьба главной героини против зловещей корпорации «Амбрелла». И не забывайте о том, что кино всегда вкуснее с Lay’s!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239240, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837736/v837736038/253bf/UAO60l99OrA.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837736/v837736038/253c0/mDwj3Z_PUlw.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837736/v837736038/253c1/YDuv7boEKRA.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837736/v837736038/253c2/lK83fuBSfsY.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837736/v837736038/253c3/cz940M3DRSo.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1487339574,
                                    'post_id': 49859, 'access_key': 'a50170850c442d3864'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 2, 'can_post': 1},
         'likes': {'count': 27, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49838, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487091511, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays\n\nПроведите этот идеальный вечер с любимыми и Lay's STAX https://vk.cc/6eU1al!",
         'attachments': [{'type': 'doc',
                          'doc': {'id': 442184293, 'owner_id': -39834333, 'title': 'Lays STAX_LOVE.gif',
                                  'size': 5177799, 'ext': 'gif',
                                  'url': 'https://vk.com/doc-39834333_442184293?hash=31ff8a692412de7451&dl=1490812907e609a9bb7254c0e12b&api=1&no_preview=1',
                                  'date': 1487089254, 'type': 3, 'preview': {'photo': {'sizes': [{
                                  'src': 'https://cs7065.userapi.com/c812226/u340295070/-3/m_39786aae65.jpg',
                                  'width': 130,
                                  'height': 100,
                                  'type': 'm'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812226/u340295070/-3/s_39786aae65.jpg',
                                      'width': 100,
                                      'height': 75,
                                      'type': 's'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812226/u340295070/-3/x_39786aae65.jpg',
                                      'width': 604,
                                      'height': 604,
                                      'type': 'x'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812226/u340295070/-3/y_39786aae65.jpg',
                                      'width': 807,
                                      'height': 807,
                                      'type': 'y'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812226/u340295070/-3/o_39786aae65.jpg',
                                      'width': 800,
                                      'height': 800,
                                      'type': 'o'}]},
                                  'video': {
                                      'src': 'https://vk.com/doc-39834333_442184293?hash=31ff8a692412de7451&dl=1490812907e609a9bb7254c0e12b&api=1&mp4=1',
                                      'width': 800,
                                      'height': 800,
                                      'file_size': 144583}},
                                  'access_key': '7e86a7cb64331ebad7'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 9, 'can_post': 1},
         'likes': {'count': 35, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 4, 'user_reposted': 0}},
        {'id': 49837, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1487089631, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nРомантичный вечер 14 февраля создан, чтобы стать особенным! А Lay’s STAX сделает восхитительный вечер еще приятнее! Только вы, она и аппетитный хрустящий Lay’s STAX… https://vk.cc/6eU1al',
         'attachments': [{'type': 'video', 'video': {'id': 456239051, 'owner_id': 340295070,
                                                     'title': "Приятное свидание вкуснее с Lay's STAX",
                                                     'duration': 20,
                                                     'description': 'Сделать приятные моменты еще более приятными… Lay’s STAX создан специально для этого! Аппетитные хрустящие ломтики и разнообразие вкусов растопят ваше сердце!',
                                                     'date': 1487088657, 'comments': 0, 'views': 137860,
                                                     'width': 1920, 'height': 1080,
                                                     'photo_130': 'https://pp.userapi.com/c626221/v626221070/58377/r1Fl_xL80c4.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c626221/v626221070/58375/lCsZuJ0PdyI.jpg',
                                                     'photo_800': 'https://pp.userapi.com/c626221/v626221070/58374/tyOA36J_MqM.jpg',
                                                     'access_key': '4db37f264480a6db2a',
                                                     'first_frame_320': 'https://pp.userapi.com/c638921/v638921070/257c4/DRsx6QzUfO0.jpg',
                                                     'first_frame_160': 'https://pp.userapi.com/c638921/v638921070/257c5/6uT3zIpNbNU.jpg',
                                                     'first_frame_130': 'https://pp.userapi.com/c638921/v638921070/257c6/nN7zNI-Dd2E.jpg',
                                                     'first_frame_800': 'https://pp.userapi.com/c638921/v638921070/257c3/HY02XihPe5c.jpg',
                                                     'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 50, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49806, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1486296019, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\n5 февраля – отличный повод отдохнуть в компании друзей, организовать викторину, разгадывать ребусы, логические задачи. Можно провести день в библиотеке или книжном магазине, познакомиться с новыми произведениями художников и посетить музеи. Мы же, в День эрудита, предлагаем увеличить свои знания о Lay’s при помощи нашей игры!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239222, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c637425/v637425070/2dbff/jSTmz8hWQIo.jpg',
                                    'photo_130': 'https://pp.userapi.com/c637425/v637425070/2dc00/I9jiaN8tynQ.jpg',
                                    'photo_604': 'https://pp.userapi.com/c637425/v637425070/2dc01/e3tDtvGUO6Y.jpg',
                                    'photo_807': 'https://pp.userapi.com/c637425/v637425070/2dc02/dC1rPvAnniE.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c637425/v637425070/2dc03/-iJouJbkhrE.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1485344884,
                                    'access_key': 'dbbce62208674c1374'}}, {'type': 'page',
                                                                           'page': {'id': 51776678,
                                                                                    'group_id': 39834333,
                                                                                    'title': "Пополни свои знания о Lay's!",
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1485339924,
                                                                                    'views': 154,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51776678?api_view=39cba59fa3c8d9938daf6535143e2b'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 7, 'can_post': 1},
         'likes': {'count': 16, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49795, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1486141581, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \nLay's STAX — долгожданная невозможно вкусная новинка уже в центре внимания!",
         'attachments': [{'type': 'video',
                          'video': {'id': 456239067, 'owner_id': -39834333, 'title': "Lay's STAX",
                                    'duration': 7, 'description': '', 'date': 1486141373, 'comments': 0,
                                    'views': 3641, 'width': 900, 'height': 900,
                                    'photo_130': 'https://pp.userapi.com/c836223/v836223333/20472/9vU2hmrLzAk.jpg',
                                    'photo_320': 'https://pp.userapi.com/c836223/v836223333/20470/efYj4Ya65L0.jpg',
                                    'photo_800': 'https://pp.userapi.com/c836223/v836223333/2046f/utXLLGR4MLk.jpg',
                                    'access_key': '638444ab9742fc65f2', 'repeat': 1,
                                    'first_frame_320': 'https://pp.userapi.com/c636622/v636622333/4f47e/6-iCfHquuCM.jpg',
                                    'first_frame_160': 'https://pp.userapi.com/c636622/v636622333/4f47f/hVSNYZAQQCQ.jpg',
                                    'first_frame_130': 'https://pp.userapi.com/c636622/v636622333/4f480/k6dw49vrCGg.jpg',
                                    'first_frame_800': 'https://pp.userapi.com/c636622/v636622333/4f47d/J3j_vxRNIOw.jpg',
                                    'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 14, 'can_post': 1},
         'likes': {'count': 31, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 3, 'user_reposted': 0}},
        {'id': 49772, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1486053152, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nУспели соскучиться по теплу? Уже сегодня сурок подскажет, как скоро наступит весна в этом году. А пока попробуйте посчитать количество вкусов Lay’s, спрятавшихся в норках нашего любимого сони! Свои варианты ответов пишите в комментариях!',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 441803843, 'owner_id': 66569038, 'title': '1_1_4.gif',
                                  'size': 7008353, 'ext': 'gif',
                                  'url': 'https://vk.com/doc66569038_441803843?hash=b773613504d9ee1cd5&dl=14908129075f13c9744589a2b7a7&api=1&no_preview=1',
                                  'date': 1486051836, 'type': 3, 'preview': {'photo': {'sizes': [
                                  {'src': 'https://pp.userapi.com/c810335/u66569038/-3/m_a08f072acf.jpg',
                                   'width': 130, 'height': 100, 'type': 'm'},
                                  {'src': 'https://pp.userapi.com/c810335/u66569038/-3/s_a08f072acf.jpg',
                                   'width': 100, 'height': 75, 'type': 's'},
                                  {'src': 'https://pp.userapi.com/c810335/u66569038/-3/x_a08f072acf.jpg',
                                   'width': 604, 'height': 604, 'type': 'x'},
                                  {'src': 'https://pp.userapi.com/c810335/u66569038/-3/y_a08f072acf.jpg',
                                   'width': 807, 'height': 807, 'type': 'y'},
                                  {'src': 'https://pp.userapi.com/c810335/u66569038/-3/o_a08f072acf.jpg',
                                   'width': 800, 'height': 800, 'type': 'o'}]}, 'video': {
                                  'src': 'https://vk.com/doc66569038_441803843?hash=b773613504d9ee1cd5&dl=14908129075f13c9744589a2b7a7&api=1&mp4=1',
                                  'width': 800, 'height': 800, 'file_size': 342491}},
                                  'access_key': '1f5bfd2958a374240e'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 29, 'can_post': 1},
         'likes': {'count': 26, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 4, 'user_reposted': 0}},
        {'id': 49764, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1485772560, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nПонедельник — день тяжёлый! Принимайте зимний челлендж от Lay’s: тегните друга, с которым хотели бы провести сегодняшний вечер в дружной компании.',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239219, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c637826/v637826038/2b4eb/Z09MAc8d2sI.jpg',
                                    'photo_130': 'https://pp.userapi.com/c637826/v637826038/2b4ec/hZCx9lQ73e8.jpg',
                                    'photo_604': 'https://pp.userapi.com/c637826/v637826038/2b4ed/qx2Ed68LiKI.jpg',
                                    'photo_807': 'https://pp.userapi.com/c637826/v637826038/2b4ee/9E1P8eRfjQQ.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c637826/v637826038/2b4ef/vG68rQvcZJw.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1484901888,
                                    'post_id': 49764, 'access_key': 'bd10d9083081436336'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 2, 'can_post': 1},
         'likes': {'count': 22, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49756, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1485596161, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong \n\nРовно 82 года назад в продаже появилось первое баночное пиво — прекрасный повод встретиться с друзьями в баре и отметить это событие вместе с Lay’s Strong!',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 441550589, 'owner_id': 66569038, 'title': 'ezgif.com-resize.gif',
                                  'size': 15714624, 'ext': 'gif',
                                  'url': 'https://vk.com/doc66569038_441550589?hash=7e96704b1460d2e554&dl=1490812907c7cf0c449bc4a55392&api=1&no_preview=1',
                                  'date': 1485507542, 'type': 3, 'preview': {'photo': {'sizes': [
                                  {'src': 'https://pp.userapi.com/c812220/u66569038/-3/m_5c5188febf.jpg',
                                   'width': 130, 'height': 100, 'type': 'm'},
                                  {'src': 'https://pp.userapi.com/c812220/u66569038/-3/s_5c5188febf.jpg',
                                   'width': 100, 'height': 75, 'type': 's'},
                                  {'src': 'https://pp.userapi.com/c812220/u66569038/-3/x_5c5188febf.jpg',
                                   'width': 604, 'height': 604, 'type': 'x'},
                                  {'src': 'https://pp.userapi.com/c812220/u66569038/-3/y_5c5188febf.jpg',
                                   'width': 807, 'height': 807, 'type': 'y'},
                                  {'src': 'https://pp.userapi.com/c812220/u66569038/-3/o_5c5188febf.jpg',
                                   'width': 600, 'height': 600, 'type': 'o'}]}, 'video': {
                                  'src': 'https://vk.com/doc66569038_441550589?hash=7e96704b1460d2e554&dl=1490812907c7cf0c449bc4a55392&api=1&mp4=1',
                                  'width': 600, 'height': 600, 'file_size': 399698}},
                                  'access_key': 'e9806ab8a81a48d064'}}, {'type': 'poll',
                                                                         'poll': {'id': 252279278,
                                                                                  'owner_id': -39834333,
                                                                                  'created': 1484901709,
                                                                                  'question': 'А какой вкус  чипсов выберете вы?',
                                                                                  'votes': 458,
                                                                                  'answer_id': 0,
                                                                                  'answers': [
                                                                                      {'id': 844252862,
                                                                                       'text': 'Охотничьи колбаски',
                                                                                       'votes': 202,
                                                                                       'rate': 44.1},
                                                                                      {'id': 844252863,
                                                                                       'text': 'Королевская креветка',
                                                                                       'votes': 170,
                                                                                       'rate': 37.12},
                                                                                      {'id': 844252864,
                                                                                       'text': 'Холодец с хреном',
                                                                                       'votes': 86,
                                                                                       'rate': 18.78}],
                                                                                  'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 23, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 4, 'user_reposted': 0}},
        {'id': 49742, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1485509762, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nИнтересный факт: ровно пятьдесят лет назад Космос был объявлен достоянием всего человечества, которое, между прочим, имеет большие планы на освоение Вселенной в этом году. А на какую планету от Lay’s отправитесь вы — на Сатурн, на Марс, на Венеру или Юпитер? Просто жмите на паузу и выкладывайте скриншот в комментарии!',
         'attachments': [{'type': 'video',
                          'video': {'id': 456239032, 'owner_id': 66569038, 'title': 'Найди свою планету!',
                                    'duration': 9, 'description': '', 'date': 1484901316, 'comments': 0,
                                    'views': 2456, 'width': 534, 'height': 552,
                                    'photo_130': 'https://pp.userapi.com/c636431/v636431038/44411/jyQT33NaAOo.jpg',
                                    'photo_320': 'https://pp.userapi.com/c636431/v636431038/4440f/nBE8Ig5-w30.jpg',
                                    'photo_800': 'https://pp.userapi.com/c636431/v636431038/4440e/cb-SQZlI2YQ.jpg',
                                    'access_key': 'eadbf903f024f6b5e5',
                                    'first_frame_320': 'https://pp.userapi.com/c604729/v604729038/3121f/xbG0tSl8G9Y.jpg',
                                    'first_frame_160': 'https://pp.userapi.com/c604729/v604729038/31220/LRKTgjofkS8.jpg',
                                    'first_frame_130': 'https://pp.userapi.com/c604729/v604729038/31221/jE_aY4I6I20.jpg',
                                    'first_frame_800': 'https://pp.userapi.com/c604729/v604729038/3121e/knHz-t_RjLg.jpg',
                                    'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 10, 'can_post': 1},
         'likes': {'count': 27, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 5, 'user_reposted': 0}},
        {'id': 49734, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1485252012, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nГотовьте свои запасы Lay’s — сегодня состоялся релиз одной из самых ожидаемых игр этого месяца — Resident Evil 7. По этому поводу мы решили составить для вас подборку лучших игр в жанре survival',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239218, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c637826/v637826038/2b4e2/M8coG-WOx5s.jpg',
                                    'photo_130': 'https://pp.userapi.com/c637826/v637826038/2b4e3/H9PXvdXvQM0.jpg',
                                    'photo_604': 'https://pp.userapi.com/c637826/v637826038/2b4e4/AMMFDMUOpRc.jpg',
                                    'photo_807': 'https://pp.userapi.com/c637826/v637826038/2b4e5/Z7CpUcnkLs0.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c637826/v637826038/2b4e6/Q0VlRi7XT44.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1484901247,
                                    'access_key': 'f4bfe8113959033e24'}}, {'type': 'page',
                                                                           'page': {'id': 51596818,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Зомби-апокалипсис',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1484920840,
                                                                                    'views': 100,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51596818?api_view=bec715e73adc398bfdaf65fe13b828'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 18, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49733, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1485180023, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong \n\nВкусы меняются, а качество остаётся неизменным!',
         'attachments': [{'type': 'doc', 'doc': {'id': 441258705, 'owner_id': 66569038, 'title': '26_1.gif',
                                                 'size': 553947, 'ext': 'gif',
                                                 'url': 'https://vk.com/doc66569038_441258705?hash=3816909b73ef30fc5b&dl=149081290761975a0bb1004149f1&api=1&no_preview=1',
                                                 'date': 1484842478, 'type': 3, 'preview': {'photo': {
                 'sizes': [
                     {'src': 'https://pp.userapi.com/c812130/u66569038/-3/m_a3a39fbc45.jpg', 'width': 130,
                      'height': 100, 'type': 'm'},
                     {'src': 'https://pp.userapi.com/c812130/u66569038/-3/s_a3a39fbc45.jpg', 'width': 100,
                      'height': 75, 'type': 's'},
                     {'src': 'https://pp.userapi.com/c812130/u66569038/-3/x_a3a39fbc45.jpg', 'width': 604,
                      'height': 604, 'type': 'x'},
                     {'src': 'https://pp.userapi.com/c812130/u66569038/-3/y_a3a39fbc45.jpg', 'width': 807,
                      'height': 807, 'type': 'y'},
                     {'src': 'https://pp.userapi.com/c812130/u66569038/-3/o_a3a39fbc45.jpg', 'width': 800,
                      'height': 800, 'type': 'o'}]}, 'video': {
                 'src': 'https://vk.com/doc66569038_441258705?hash=3816909b73ef30fc5b&dl=149081290761975a0bb1004149f1&api=1&mp4=1',
                 'width': 800, 'height': 800, 'file_size': 141606}}, 'access_key': 'bbcf383e012ae2145d'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 18, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49732, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1485174871, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nКомпания PepsiCo стремится дарить людям улыбки каждый день. Поэтому первого января в Москве прошла акция «Начни год с улыбки». Жители города могли бесплатно проехать в такси, заплатив своей улыбкой, а также получить вкусные подарки от Lay’s!',
         'attachments': [{'type': 'video',
                          'video': {'id': 456239066, 'owner_id': -39834333, 'title': 'Начни год с улыбки',
                                    'duration': 125,
                                    'description': 'Компания PepsiCo стремится дарить людям улыбки каждый день, поэтому первого января в Москве прошла акция «Начни год с улыбки». Жители города могли бесплатно проехать в такси, заплатив своей улыбкой',
                                    'date': 1485174871, 'comments': 0, 'views': 680319,
                                    'photo_130': 'https://pp.userapi.com/c638129/u20153805/video/s_09e5698e.jpg',
                                    'photo_320': 'https://pp.userapi.com/c638129/u20153805/video/l_e249d175.jpg',
                                    'photo_640': 'https://pp.userapi.com/c638129/u20153805/video/y_38d219d5.jpg',
                                    'access_key': '96e9df11caaaad6c32', 'platform': 'YouTube',
                                    'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 15, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49712, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1484843195, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nСамое время выбрать свою сторону в межгалактической войне и привести её к победе — вчера состоялся долгожданный релиз игры Warhammer 40000 Sanctus Reach. \nПо этому случаю предлагаем вам ознакомиться с подборкой самых интересных тактических стратегий!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239217, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c626427/v626427038/4cb1e/esSQQKXOi3I.jpg',
                                    'photo_130': 'https://pp.userapi.com/c626427/v626427038/4cb1f/FMPJJs7Rp_o.jpg',
                                    'photo_604': 'https://pp.userapi.com/c626427/v626427038/4cb20/iJatI4QM8xU.jpg',
                                    'photo_807': 'https://pp.userapi.com/c626427/v626427038/4cb21/zqAh6DLHot4.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c626427/v626427038/4cb22/o1HwLPJzq0E.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1484841597,
                                    'access_key': 'db6240e14b9a45d578'}}, {'type': 'page',
                                                                           'page': {'id': 51593610,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Зарядка для ума',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1484839546,
                                                                                    'views': 72,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51593610?api_view=a09519e21606edfa1daf60ded3e280'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 19, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49702, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1484829861, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\n«Три икса: Мировое господство» наконец-то в прокате — Вин Дизель и его команда отъявленных экстремалов объединяются для спасения всего человечества от нового опасного оружия – Ящика Пандоры. Скорей отменяй все дела и беги спасать мир вместе с пачкой Lay’s!',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 441248864, 'owner_id': 66569038, 'title': 'Diesel.gif',
                                  'size': 1003107, 'ext': 'gif',
                                  'url': 'https://vk.com/doc66569038_441248864?hash=fb74b05aba85c5cff0&dl=149081290794ad87d8e20385a078&api=1&no_preview=1',
                                  'date': 1484829687, 'type': 3, 'preview': {'photo': {'sizes': [{
                                  'src': 'https://cs7065.userapi.com/c812423/u340295070/-3/m_1b762d87d0.jpg',
                                  'width': 130,
                                  'height': 100,
                                  'type': 'm'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812423/u340295070/-3/s_1b762d87d0.jpg',
                                      'width': 100,
                                      'height': 75,
                                      'type': 's'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812423/u340295070/-3/x_1b762d87d0.jpg',
                                      'width': 604,
                                      'height': 604,
                                      'type': 'x'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812423/u340295070/-3/y_1b762d87d0.jpg',
                                      'width': 807,
                                      'height': 807,
                                      'type': 'y'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c812423/u340295070/-3/o_1b762d87d0.jpg',
                                      'width': 600,
                                      'height': 600,
                                      'type': 'o'}]},
                                  'video': {
                                      'src': 'https://vk.com/doc66569038_441248864?hash=fb74b05aba85c5cff0&dl=149081290794ad87d8e20385a078&api=1&mp4=1',
                                      'width': 600,
                                      'height': 600,
                                      'file_size': 52104}},
                                  'access_key': '546ff2bf26cf605c85'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 12, 'can_post': 1},
         'likes': {'count': 19, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49605, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483959625, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #футболвкуснеесLays \n\nОтгремел Чемпионат Европы 2016, национальные первенства и еврокубки взяли тайм-аут. Наступило время подведения итогов футбольного года. Сегодня в Цюрихе будет вручена очень престижная премия «Золотой мяч» 2017. Трофей присуждается лучшему футболисту прошедшего года. Кроме этой награды, организаторы намерены чествовать лучшего тренера женской команды и самого успешного наставника мужского коллектива, а также футболиста, который забил самый красивый гол в 2016 году. Но венцом торжественной церемонии всё же станет вручение \u200b\u200b«Золотого мяча»! \nКто по итогам опросов попадёт в десятку лучших, нам пока неизвестно. Однако, их список нетрудно составить, ибо все мы являлись очевидцами самых громких футбольных событий года.\u200b Чтобы скрасить ожидание, запаситесь чипсами.',
         'attachments': [{'type': 'video',
                          'video': {'id': 456239049, 'owner_id': 340295070, 'title': 'Золотой мяч',
                                    'duration': 9, 'description': '', 'date': 1483106582, 'comments': 0,
                                    'views': 1868, 'width': 800, 'height': 800,
                                    'photo_130': 'https://pp.userapi.com/c636617/v636617070/3f6db/x0c1lrEJ0TI.jpg',
                                    'photo_320': 'https://pp.userapi.com/c636617/v636617070/3f6d9/-ZJYGAQG4YY.jpg',
                                    'photo_800': 'https://pp.userapi.com/c636617/v636617070/3f6d8/_4YgfRYUrsY.jpg',
                                    'access_key': 'd6d96776c680913d8f', 'repeat': 1,
                                    'first_frame_320': 'https://pp.userapi.com/c836121/v836121070/16246/R35dwVIdyRs.jpg',
                                    'first_frame_160': 'https://pp.userapi.com/c836121/v836121070/16247/Xjva3aMVVC4.jpg',
                                    'first_frame_130': 'https://pp.userapi.com/c836121/v836121070/16248/Zm-t4GWDa_k.jpg',
                                    'first_frame_800': 'https://pp.userapi.com/c836121/v836121070/16245/_JvHmGroYh4.jpg',
                                    'can_add': 1}}, {'type': 'poll',
                                                     'poll': {'id': 249742660, 'owner_id': -39834333,
                                                              'created': 1483106682,
                                                              'question': 'За кого вы отдали бы свой голос?',
                                                              'votes': 541, 'answer_id': 0, 'answers': [
                                                             {'id': 835344860, 'text': 'Лионель Месси',
                                                              'votes': 240, 'rate': 44.36},
                                                             {'id': 835344861, 'text': 'Криштиану Роналду',
                                                              'votes': 157, 'rate': 29.02},
                                                             {'id': 835344862, 'text': 'Антуан Гризманн',
                                                              'votes': 26, 'rate': 4.81},
                                                             {'id': 835344863, 'text': 'Гарет Бейл',
                                                              'votes': 12, 'rate': 2.22},
                                                             {'id': 835344864, 'text': 'Луис Суарес',
                                                              'votes': 18, 'rate': 3.33},
                                                             {'id': 835344865, 'text': 'Мануэль Нойер',
                                                              'votes': 14, 'rate': 2.59},
                                                             {'id': 835344866, 'text': 'Неймар',
                                                              'votes': 38, 'rate': 7.02},
                                                             {'id': 835344867, 'text': 'Лука Модрич',
                                                              'votes': 9, 'rate': 1.66},
                                                             {'id': 835344868, 'text': 'Хави Иньеста',
                                                              'votes': 12, 'rate': 2.22},
                                                             {'id': 835344869, 'text': 'Томас Мюллер',
                                                              'votes': 15, 'rate': 2.77}],
                                                              'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 12, 'can_post': 1},
         'likes': {'count': 23, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49470, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483869618, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong \n\nПоследний \u200bпраздничный день\u200b\u200b — отличный повод вспомнить, что вы сделали из программы «Обязательно успеть \u200bв новогодние праздники». По этому случаю предлагаем вам сыграть в филворд, где загаданы подсказки о самых \u200bзимних \u200bразвлечениях.\u200b \u200b \n \nПишите в комментариях слова и комбинации слов из одной строчки, а уже в начале следующей недели мы объявим победителя!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239127, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://cs7065.userapi.com/c604717/v604717070/208dd/ZOvjVmPiHh0.jpg',
                                    'photo_130': 'https://cs7065.userapi.com/c604717/v604717070/208de/4B9Ws6jzAvM.jpg',
                                    'photo_604': 'https://cs7065.userapi.com/c604717/v604717070/208df/jbwdCH5xQ1c.jpg',
                                    'photo_807': 'https://cs7065.userapi.com/c604717/v604717070/208e0/I47qin7Pxl0.jpg',
                                    'photo_1280': 'https://cs7065.userapi.com/c604717/v604717070/208e1/EQ5MNbCb77A.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1483106209,
                                    'post_id': 49470, 'access_key': '54bb0ac40b40e54763'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 134, 'can_post': 1},
         'likes': {'count': 29, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 3, 'user_reposted': 0}},
        {'id': 49401, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483779638, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays\n\nМы поздравляем вас с Рождеством и желаем провести этот вечер в хорошей компании с душевными разговорами под хруст Lay’s!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239126, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://cs7065.userapi.com/c604717/v604717070/208d5/PsZvNx-qD8Y.jpg',
                                    'photo_130': 'https://cs7065.userapi.com/c604717/v604717070/208d6/Jr79e-g28QQ.jpg',
                                    'photo_604': 'https://cs7065.userapi.com/c604717/v604717070/208d7/hsy1FgAjXw0.jpg',
                                    'photo_807': 'https://cs7065.userapi.com/c604717/v604717070/208d8/JdS2EXQmfPU.jpg',
                                    'width': 800, 'height': 800, 'text': '', 'date': 1483106165,
                                    'post_id': 49401, 'access_key': 'd800dbabcb1f3c12af'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 16, 'can_post': 1},
         'likes': {'count': 51, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49382, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483614040, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nОдно из ярких событий этих зимних каникул — выход на экран полнометражного фильма «Кредо убийцы». Ликуйте, поклонники культовой игры Assassin’s Creed! Теперь вы сможете насладиться захватывающим сюжетом и отменной компьютерной графикой, которую разработали\u200b лучшие специалисты Голливуда. Давайте вместе вспомним и другие крутые картины, снятые по мотивам культовых игр!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239125, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://cs7065.userapi.com/c604717/v604717070/208cc/1xvlurK4GIE.jpg',
                                    'photo_130': 'https://cs7065.userapi.com/c604717/v604717070/208cd/8Szlu50S4Tg.jpg',
                                    'photo_604': 'https://cs7065.userapi.com/c604717/v604717070/208ce/W6pObyoIDzM.jpg',
                                    'photo_807': 'https://cs7065.userapi.com/c604717/v604717070/208cf/gnHDQBOjb88.jpg',
                                    'photo_1280': 'https://cs7065.userapi.com/c604717/v604717070/208d0/Y9KzXysweO8.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1483106027,
                                    'access_key': 'b04bef4213ed00d708'}}, {'type': 'page',
                                                                           'page': {'id': 51521608,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Подборка фильмов по сюжетам известных игр',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1483103997,
                                                                                    'views': 151,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51521608?api_view=16e0b2deb7e369e17daf678460219d'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 27, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 3, 'user_reposted': 0}},
        {'id': 49373, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483538569, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': 'Беззаботно смотреть любимые сериалы вместе с близкими людьми - бесценно. Lay’s STAX с нежным вкусом краба сделает приятные моменты еще приятнее. Больше информации о продукте: stax.lays.ru',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239138, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c626530/v626530531/58fb0/19ZsYunnMk4.jpg',
                                    'photo_130': 'https://pp.userapi.com/c626530/v626530531/58fb1/qvdYxTKFm3U.jpg',
                                    'photo_604': 'https://pp.userapi.com/c626530/v626530531/58fb2/50SvcMzyav8.jpg',
                                    'photo_807': 'https://pp.userapi.com/c626530/v626530531/58fb3/OSjNM9EE0MU.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c626530/v626530531/58fb4/O5_W78yB9fo.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1483530895,
                                    'post_id': 49373, 'access_key': '5975def7261898ea01'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 34, 'can_post': 1},
         'likes': {'count': 186, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 6, 'user_reposted': 0}},
        {'id': 49371, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483527602, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n \nСегодня весь научный мир отмечает день Ньютона, и Lay’s присоединяется к этому празднику. Полагаем, что историю об озарившем учёного яблоке слышали уже все. Однако не каждый знает о том, что в честь великого гения были названы не только законы и уравнения, но и элитный сорт картофеля!',
         'attachments': [{'type': 'video',
                          'video': {'id': 456239047, 'owner_id': 340295070, 'title': 'Newton',
                                    'duration': 4, 'description': '', 'date': 1483105052, 'comments': 0,
                                    'views': 2241, 'width': 1000, 'height': 1000,
                                    'photo_130': 'https://pp.userapi.com/c836421/v836421070/b5aef/9Ay-HVgiG4M.jpg',
                                    'photo_320': 'https://pp.userapi.com/c836421/v836421070/b5aed/563e_jhhIAU.jpg',
                                    'photo_800': 'https://pp.userapi.com/c836421/v836421070/b5aec/u9C_AeNI5Po.jpg',
                                    'access_key': '356ac06ae50fa7c559', 'repeat': 1,
                                    'first_frame_320': 'https://pp.userapi.com/c636217/v636217070/4a903/M5pHCqHYbsc.jpg',
                                    'first_frame_160': 'https://pp.userapi.com/c636217/v636217070/4a904/EpYaVrRInSQ.jpg',
                                    'first_frame_130': 'https://pp.userapi.com/c636217/v636217070/4a905/eQVuP-e_pzo.jpg',
                                    'first_frame_800': 'https://pp.userapi.com/c636217/v636217070/4a902/nlr_aqPNoBU.jpg',
                                    'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 1, 'can_post': 1},
         'likes': {'count': 27, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49369, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483452009, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': 'Вечер с любимыми, разговор по душам, настроение праздника… Наслаждайтесь приятными моментами вместе с Lay’s STAX. Больше информации о продукте: stax.lays.ru',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239131, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://cs7065.userapi.com/c604717/v604717070/20924/e1EGVlXRI_c.jpg',
                                    'photo_130': 'https://cs7065.userapi.com/c604717/v604717070/20925/UTIGNRRF2DE.jpg',
                                    'photo_604': 'https://cs7065.userapi.com/c604717/v604717070/20926/e8CRNIxQ-wc.jpg',
                                    'photo_807': 'https://cs7065.userapi.com/c604717/v604717070/20927/galeyNJYQK8.jpg',
                                    'photo_1280': 'https://cs7065.userapi.com/c604717/v604717070/20928/TodMyr5DGBw.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1483113396,
                                    'access_key': 'dd6c414485246db0be'}}, {'type': 'link', 'link': {
             'url': 'http://stax.lays.ru', 'title': "Lay's STAX", 'description': '',
             'target': 'external'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 3, 'can_post': 1},
         'likes': {'count': 132, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 3, 'user_reposted': 0}},
        {'id': 49367, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483437613, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nЛюбимое кино уже пересмотрено несколько раз, многочисленные закуски и салаты доедены, и пора выбираться из дома. Зимняя Москва предлагает множество развлечений жителям и гостям. Одним из самых запоминающихся мероприятий может стать для вас поход на выставку ледяных скульптур. А какие развлечения есть в ваших городах? Если вы не из столицы, то пишите в комментарии, какие интересные места и события можно посетить в вашем городе во время январских праздников, взяв с собой Lay’s!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239123, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://cs7065.userapi.com/c604717/v604717070/2089e/bYlSbTCAcmA.jpg',
                                    'photo_130': 'https://cs7065.userapi.com/c604717/v604717070/2089f/oM6k0QALZIA.jpg',
                                    'photo_604': 'https://cs7065.userapi.com/c604717/v604717070/208a0/_GwYJZv9eEs.jpg',
                                    'photo_807': 'https://cs7065.userapi.com/c604717/v604717070/208a1/SZy_i8UOnqI.jpg',
                                    'photo_1280': 'https://cs7065.userapi.com/c604717/v604717070/208a2/Zudf87XMeCM.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1483104982,
                                    'access_key': '2102e583ebb64a7589'}}, {'type': 'page',
                                                                           'page': {'id': 51521591,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Ледяные скульптуры в Москве 2017',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1483103550,
                                                                                    'views': 58,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51521591?api_view=876881d4f25980986daf6f07508413'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 1, 'can_post': 1},
         'likes': {'count': 18, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49355, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483365620, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': 'Зимние каникулы – время удовольствия. Морозный горный воздух, роскошный вид и хрустящие Lay’s STAX с солью – рецепт счастливого дня. Больше информации о продукте: stax.lays.ru',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239129, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://cs7065.userapi.com/c604717/v604717070/20912/6qya7rCdmWY.jpg',
                                    'photo_130': 'https://cs7065.userapi.com/c604717/v604717070/20913/_mMVs0aB-TQ.jpg',
                                    'photo_604': 'https://cs7065.userapi.com/c604717/v604717070/20914/NHBLmd59ld0.jpg',
                                    'photo_807': 'https://cs7065.userapi.com/c604717/v604717070/20915/iGcNQOmlXo0.jpg',
                                    'photo_1280': 'https://cs7065.userapi.com/c604717/v604717070/20916/x7P60F5vDMw.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1483113203,
                                    'access_key': '89dcb9c1dd7719caeb'}}, {'type': 'link', 'link': {
             'url': 'http://stax.lays.ru', 'title': "Lay's STAX", 'description': '',
             'target': 'external'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 6, 'can_post': 1},
         'likes': {'count': 207, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 14, 'user_reposted': 0}},
        {'id': 49345, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483279226, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': 'Энрике Иглесиас представляет уникальную новинку – хрустящие и аппетитные Lay’s STAX, и желает, чтобы все приятные моменты на каникулах были по-настоящему особенными! Больше информации о продукте: stax.lays.ru',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239128, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://cs7065.userapi.com/c604717/v604717070/20909/L97eavTte1A.jpg',
                                    'photo_130': 'https://cs7065.userapi.com/c604717/v604717070/2090a/hBNurpFUmQU.jpg',
                                    'photo_604': 'https://cs7065.userapi.com/c604717/v604717070/2090b/MSqin4e9-60.jpg',
                                    'photo_807': 'https://cs7065.userapi.com/c604717/v604717070/2090c/kr_jKZ1HYek.jpg',
                                    'photo_1280': 'https://cs7065.userapi.com/c604717/v604717070/2090d/Ut7OgBAN9YE.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1483113167,
                                    'access_key': '1d55a0e3cfcb3931c7'}}, {'type': 'link', 'link': {
             'url': 'http://stax.lays.ru', 'title': "Lay's STAX", 'description': '',
             'target': 'external'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 6, 'can_post': 1},
         'likes': {'count': 1583, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 35, 'user_reposted': 0}},
        {'id': 49344, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483261248, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nУже проснулись после новогодней ночи? Январь несёт много «вкусного» любителям сериального жанра и обещает, что мы не один раз «выпадем» из жизни, увлечённо наблюдая за персонажами. Лучшее лекарство от последствий праздника — начало 4 сезона сериала «Шерлок». Три года ожидания завершаются пиршеством из трёх новых серий. Сегодня первая!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239122, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://cs7065.userapi.com/c604717/v604717070/20895/TnCJnlUIKpA.jpg',
                                    'photo_130': 'https://cs7065.userapi.com/c604717/v604717070/20896/ZP7aiPWox6A.jpg',
                                    'photo_604': 'https://cs7065.userapi.com/c604717/v604717070/20897/y0oaf3I3E0k.jpg',
                                    'photo_807': 'https://cs7065.userapi.com/c604717/v604717070/20898/B5tXy8T--k8.jpg',
                                    'photo_1280': 'https://cs7065.userapi.com/c604717/v604717070/20899/eXZp99dZvQ8.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1483104296,
                                    'post_id': 49344, 'access_key': 'b0a431b0adc0c991f4'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 14, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49342, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483217946, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nПоздравляем с Новым годом! \nПусть 2017 год станет лучше, чем високосный 2016, и рядом с вами всегда будут искренние, надежные друзья. \n\nВстречайте этот праздник с улыбкой!',
         'attachments': [{'type': 'video',
                          'video': {'id': 456239046, 'owner_id': 340295070, 'title': 'С Новым годом!',
                                    'duration': 8, 'description': '', 'date': 1480692795, 'comments': 0,
                                    'views': 2054, 'width': 800, 'height': 800,
                                    'photo_130': 'https://pp.userapi.com/c637421/v637421070/1d95b/Jk8nn8jR3jw.jpg',
                                    'photo_320': 'https://pp.userapi.com/c637421/v637421070/1d959/fencQHWf3Yo.jpg',
                                    'photo_800': 'https://pp.userapi.com/c637421/v637421070/1d958/6GqAuvPTjlc.jpg',
                                    'access_key': '9d54e3e77d1ad4fd39', 'repeat': 1,
                                    'first_frame_320': 'https://pp.userapi.com/c636628/v636628070/3de64/WOSvnrCJfAY.jpg',
                                    'first_frame_160': 'https://pp.userapi.com/c636628/v636628070/3de65/4Iszzxoj7rY.jpg',
                                    'first_frame_130': 'https://pp.userapi.com/c636628/v636628070/3de66/nkYhP25BsS0.jpg',
                                    'first_frame_800': 'https://pp.userapi.com/c636628/v636628070/3de63/o2yOkk5tt94.jpg',
                                    'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 1, 'can_post': 1},
         'likes': {'count': 32, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49335, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483171207, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong \n\nКак Новый год встретишь, так его и проведешь… Поэтому сегодня вечером на ваших столах должны оказаться чипсы Lay’s Strong, чтобы 2017 стал вкусным и прошел в компании лучших друзей!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239065, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837238/v837238070/1a8ec/QR4cBZeDIFM.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837238/v837238070/1a8ed/okNb_pTCQnc.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837238/v837238070/1a8ee/16iNxkT32o0.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837238/v837238070/1a8ef/MaMB99Eil5o.jpg',
                                    'width': 800, 'height': 800, 'text': '', 'date': 1480692681,
                                    'post_id': 49335, 'access_key': 'e73278d58fac8d9fa4'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 8, 'can_post': 1},
         'likes': {'count': 19, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49318, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1483081211, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays\n\nУже завтра столы в каждом доме будут заставлены новогодними блюдами. Чтобы там оказалось что-то кроме оливье и селёдки под шубой, мы предлагаем вам пойти нестандартным путём и сделать печенье из чипсов: https://vk.cc/5Stmeb.  Приятного аппетита!\nВыиграйте новогодние призы, все лишь зарегистрировав код по ссылке: nysmile.ru!\n*Общий срок проведения акции — с 01.11.2016 по 10.02.2017, включая период выдачи призов победителям. Подробности на nysmile.ru.',
         'attachments': [{'type': 'video', 'video': {'id': 456239045, 'owner_id': 340295070,
                                                     'title': 'Сырное печенье с Lays', 'duration': 74,
                                                     'description': '', 'date': 1480692390, 'comments': 0,
                                                     'views': 1460, 'width': 1280, 'height': 720,
                                                     'photo_130': 'https://pp.userapi.com/c636029/v636029070/3da75/zaReG5b4jSw.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c636029/v636029070/3da73/QJUBAEpksOo.jpg',
                                                     'photo_800': 'https://pp.userapi.com/c636029/v636029070/3da72/cP0j40XnV_0.jpg',
                                                     'access_key': 'a1468ce1a2055962eb',
                                                     'first_frame_320': 'https://pp.userapi.com/c626724/v626724070/352a5/qiqIPEl4b50.jpg',
                                                     'first_frame_160': 'https://pp.userapi.com/c626724/v626724070/352a6/CZHb-QUpuYQ.jpg',
                                                     'first_frame_130': 'https://pp.userapi.com/c626724/v626724070/352a7/I-382I7l21M.jpg',
                                                     'first_frame_800': 'https://pp.userapi.com/c626724/v626724070/352a4/frsTvkvREQk.jpg',
                                                     'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 1, 'can_post': 1},
         'likes': {'count': 19, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49309, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1482948009, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nНовый год без новогоднего кино уже немыслим! Зачем ждать 31 декабря и выходных, чтобы вновь почувствовать себя как в детстве и радоваться Новому году :)',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239089, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837324/v837324531/18c12/_6wZc480RK0.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837324/v837324531/18c13/-2onndyYkh0.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837324/v837324531/18c14/OAhZfcPHOaA.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837324/v837324531/18c15/r1w89Cld9qk.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837324/v837324531/18c16/rVcKT6q_Cjg.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1481289191,
                                    'access_key': '9daffde9e87e73ce82'}}, {'type': 'page',
                                                                           'page': {'id': 51222174,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Новогодние фильмы',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1481213189,
                                                                                    'views': 69,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51222174?api_view=deb7495d5d949cbdfdaf62fbd81924'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 8, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49296, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1482858009, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nЕсли у вас всё еще нет Новогоднего настроения, то пора что-то менять… Например, внешний вид квартиры или дома. Специально для вас мы подготовили несколько простых, но очень красивых способа создания новогодних украшений: https://vk.cc/5SrEXX. \n \nЗарегистрируйте код по ссылке: nysmile.ru и выиграйте новогодние призы! \n \n*Общий срок проведения акции — с 01.11.2016 по 10.02.2017, включая период выдачи призов победителям. Подробности на nysmile.ru.',
         'attachments': [{'type': 'video', 'video': {'id': 456239043, 'owner_id': 340295070,
                                                     'title': 'Как украсить дом к празднику',
                                                     'duration': 191, 'description': '', 'date': 1480691262,
                                                     'comments': 0, 'views': 1481, 'width': 1280,
                                                     'height': 720,
                                                     'photo_130': 'https://pp.userapi.com/c637218/v637218070/217d1/ZYBpWjOYTs4.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c637218/v637218070/217cf/OMHax4zd36Y.jpg',
                                                     'photo_800': 'https://pp.userapi.com/c637218/v637218070/217ce/VFbjkMOWSS0.jpg',
                                                     'access_key': 'f7a94dfb2bd058c327',
                                                     'first_frame_320': 'https://pp.userapi.com/c636917/v636917070/3acde/Ub_4d6sydF4.jpg',
                                                     'first_frame_160': 'https://pp.userapi.com/c636917/v636917070/3acdf/eMg2ri7TlVo.jpg',
                                                     'first_frame_130': 'https://pp.userapi.com/c636917/v636917070/3ace0/z3ONUS7md5E.jpg',
                                                     'first_frame_800': 'https://pp.userapi.com/c636917/v636917070/3acdd/6Pf6_wrWvzU.jpg',
                                                     'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 18, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49231, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1482602406, 'marked_as_ads': 0,
         'post_type': 'post', 'text': '#каждыйденьвкуснеесLays #Strong', 'attachments': [{'type': 'video',
                                                                                          'video': {
                                                                                              'id': 456239064,
                                                                                              'owner_id': -39834333,
                                                                                              'title': 'Любимый вкус',
                                                                                              'duration': 6,
                                                                                              'description': '',
                                                                                              'date': 1480690236,
                                                                                              'comments': 0,
                                                                                              'views': 2949,
                                                                                              'width': 800,
                                                                                              'height': 800,
                                                                                              'photo_130': 'https://pp.userapi.com/c837430/v837430333/106d9/ngMUR0zOKeU.jpg',
                                                                                              'photo_320': 'https://pp.userapi.com/c837430/v837430333/106d7/0q7qJERal4U.jpg',
                                                                                              'photo_800': 'https://pp.userapi.com/c837430/v837430333/106d6/QWZXp1YDbgA.jpg',
                                                                                              'access_key': 'c6f2232063f13e6e39',
                                                                                              'repeat': 1,
                                                                                              'first_frame_320': 'https://pp.userapi.com/c836235/v836235333/f05e/7tnNt_IManI.jpg',
                                                                                              'first_frame_160': 'https://pp.userapi.com/c836235/v836235333/f05f/QWBX58Fi754.jpg',
                                                                                              'first_frame_130': 'https://pp.userapi.com/c836235/v836235333/f060/pbcPhNryNxg.jpg',
                                                                                              'first_frame_800': 'https://pp.userapi.com/c836235/v836235333/f05d/AQT5Bp8yuPI.jpg',
                                                                                              'can_add': 1}},
                                                                                         {'type': 'poll',
                                                                                          'poll': {
                                                                                              'id': 246619911,
                                                                                              'owner_id': -39834333,
                                                                                              'created': 1480690892,
                                                                                              'question': 'Кто из них был у вас первым? Какой вкус вы попробовали раньше остальных?',
                                                                                              'votes': 591,
                                                                                              'answer_id': 0,
                                                                                              'answers': [{
                                                                                                  'id': 824375831,
                                                                                                  'text': 'Охотничьи колбаски',
                                                                                                  'votes': 306,
                                                                                                  'rate': 51.78},
                                                                                                  {
                                                                                                      'id': 824375832,
                                                                                                      'text': 'Королевская креветка',
                                                                                                      'votes': 173,
                                                                                                      'rate': 29.27},
                                                                                                  {
                                                                                                      'id': 824375833,
                                                                                                      'text': 'Холодец с хреном',
                                                                                                      'votes': 112,
                                                                                                      'rate': 18.95}],
                                                                                              'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 7, 'can_post': 1},
         'likes': {'count': 66, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 4, 'user_reposted': 0}},
        {'id': 49211, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1482429604, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nУже купили все подарки? Если нет, то у вас еще есть время до Нового года, а если да, то их следует правильно завернуть. Не знаете как? Тогда мы правильно сделали, что подготовили подробную инструкцию: https://vk.cc/5SrEXX. \n \nЗарегистрируйте код по ссылке: nysmile.ru и выиграйте новогодние призы! \n \n*Общий срок проведения акции — с 01.11.2016 по 10.02.2017, включая период выдачи призов победителям. Подробности на nysmile.ru.',
         'attachments': [{'type': 'video', 'video': {'id': 456239039, 'owner_id': 340295070,
                                                     'title': 'Как упаковать новогодний подарок',
                                                     'duration': 148, 'description': '', 'date': 1480688693,
                                                     'comments': 0, 'views': 1734, 'width': 1280,
                                                     'height': 720,
                                                     'photo_130': 'https://pp.userapi.com/c626319/v626319070/3b9b6/bx6GBXua4Xs.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c626319/v626319070/3b9b4/gI4UmledEgA.jpg',
                                                     'photo_800': 'https://pp.userapi.com/c626319/v626319070/3b9b3/BetSBjhkeqY.jpg',
                                                     'access_key': '76f83f0d3e76a6fc3a',
                                                     'first_frame_320': 'https://cs7065.userapi.com/c638719/v638719070/16f68/1LpSz6EXxKU.jpg',
                                                     'first_frame_160': 'https://cs7065.userapi.com/c638719/v638719070/16f69/dIQ3o0gnkAE.jpg',
                                                     'first_frame_130': 'https://cs7065.userapi.com/c638719/v638719070/16f6a/9wkq5WP3o-c.jpg',
                                                     'first_frame_800': 'https://cs7065.userapi.com/c638719/v638719070/16f67/nfqTTlo2aek.jpg',
                                                     'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 23, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 3, 'user_reposted': 0}},
        {'id': 49207, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1482412866, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nУлицы городов украшаются к Новому Году с самого начала декабря. Пора постепенно задумываться и о домашней праздничной обстановке. Вам наскучили привычные ёлочные игрушки? Предлагаем в этом году украсить ёлку по-новому🎄 :)',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239103, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c637226/v637226531/2b0c9/wVHY_SNIkpI.jpg',
                                    'photo_130': 'https://pp.userapi.com/c637226/v637226531/2b0ca/JLDx31bfLCM.jpg',
                                    'photo_604': 'https://pp.userapi.com/c637226/v637226531/2b0cb/137w6R4RRVY.jpg',
                                    'photo_807': 'https://pp.userapi.com/c637226/v637226531/2b0cc/4ONRTtzCuOQ.jpg',
                                    'width': 800, 'height': 800, 'text': '', 'date': 1482412866,
                                    'post_id': 49207, 'access_key': '45a6a6964f30817998'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 10, 'can_post': 1},
         'likes': {'count': 27, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49185, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1482217224, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#футболвкуснеесLays \n\nДо следующих матчей Лиги Чемпионов УЕФА ждать еще очень долго. Поэтому давайте компенсируем это время хорошими футбольными историями.',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239090, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837324/v837324531/18c78/nNPRBDGaDyA.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837324/v837324531/18c79/2zA0ba2tzjI.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837324/v837324531/18c7a/sU9S0hrvdRE.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837324/v837324531/18c7b/UCQxPKGIXmI.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837324/v837324531/18c7c/6L_ZTcgPWK8.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1481293779,
                                    'access_key': '4da70f85e64c5eecc3'}}, {'type': 'page',
                                                                           'page': {'id': 51225188,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Интересные футбольные факты',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1481293513,
                                                                                    'views': 45,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51225188?api_view=2e329484dc18c322fdaf6aa6058fc3'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 11, 'can_post': 1},
         'likes': {'count': 9, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49174, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1481972429, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong \n\nА вы знали, что 17 декабря 1989 года вышла первая серия «Симпсонов", невольно предсказавших многие события задолго до того, как они произошли на самом деле!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239077, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837323/v837323531/1318a/vppcFzAXmkE.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837323/v837323531/1318b/NSpqHELpyaI.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837323/v837323531/1318c/yYfIVE3exXk.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837323/v837323531/1318d/FCHsFRZgwzI.jpg',
                                    'width': 800, 'height': 800, 'text': '', 'date': 1481209317,
                                    'post_id': 49174, 'access_key': '415ea0b8cde63da2dd'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 32, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49159, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1481785205, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nСегодня большой день для всех фанатов «Звёздных войн» - премьера фильма «Изгой-один: Звёздные войны. Истории». Что нам ждать от нового эпизода, какие пасхалки приготовили для зрителей читайте в нашей подборке!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239087, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837324/v837324531/18c00/O-K2Op8-kJE.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837324/v837324531/18c01/NkKr4yZdVvw.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837324/v837324531/18c02/nVe0uLu1050.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837324/v837324531/18c03/Hr9IkTk6eyk.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837324/v837324531/18c04/y091AJvAV6k.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1481288519,
                                    'access_key': '8f64f0f4752e041d3e'}}, {'type': 'page',
                                                                           'page': {'id': 51222161,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Изгой-один: Звёздные войны',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1481212983,
                                                                                    'views': 78,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51222161?api_view=bdb78015aaa5fdbbcdaf62f74c9377'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 9, 'can_post': 1},
         'likes': {'count': 14, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49154, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1481648426, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nЗимой нужно уметь правильно быстро согреваться, иначе рискуете простудиться и заболеть аккурат к Новому году. Чтобы этого избежать, следуйте инструкциям по ссылке: https://vk.cc/5RZvYm. \n \nВыигрывайте призы в Новогоднем конкурсе! Нужно просто зарегистрировать код по ссылке: nysmile.ru. \n \n*Общий срок проведения акции — с 01.11.2016 по 10.02.2017, включая период выдачи призов победителям. Подробности на nysmile.ru.',
         'attachments': [{'type': 'video', 'video': {'id': 456239040, 'owner_id': 340295070,
                                                     'title': 'Как быстро согреться зимой', 'duration': 62,
                                                     'description': '', 'date': 1480688707, 'comments': 0,
                                                     'views': 1596, 'width': 1280, 'height': 720,
                                                     'photo_130': 'https://pp.userapi.com/c837626/v837626070/10584/tr9PN-8CrRQ.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c837626/v837626070/10582/BAlS56z9Dxg.jpg',
                                                     'photo_800': 'https://pp.userapi.com/c837626/v837626070/10581/iZ9dLiMfw18.jpg',
                                                     'access_key': '1d94f2f1bcedc5abdd',
                                                     'first_frame_320': 'https://pp.userapi.com/c837230/v837230070/daff/Ca-c2sL-xKo.jpg',
                                                     'first_frame_160': 'https://pp.userapi.com/c837230/v837230070/db00/cILT1EiUd7Y.jpg',
                                                     'first_frame_130': 'https://pp.userapi.com/c837230/v837230070/db01/rt79QeVmrIs.jpg',
                                                     'first_frame_800': 'https://pp.userapi.com/c837230/v837230070/dafe/0fUwBpJueeU.jpg',
                                                     'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 20, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49132, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1481349677, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#футболвкуснеесLays \n\nСегодня - Всемирный день футбола. Если вы не знакомы с историей самого популярного вида спорта, то пора просвещаться!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239086, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837324/v837324531/18bf3/1rxCgqjrsxs.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837324/v837324531/18bf4/hCbP7jDa7xU.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837324/v837324531/18bf5/p1_GDgc3PwQ.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837324/v837324531/18bf6/xVYiBPsM30Y.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837324/v837324531/18bf7/93Rw8ejNgxM.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1481288165,
                                    'access_key': '76e24e4e224cdc381e'}}, {'type': 'page',
                                                                           'page': {'id': 51222166,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Футбол в мировой истории',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1481213104,
                                                                                    'views': 53,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51222166?api_view=b7166d2239c8690b6daf68e99fe75d'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 13, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49112, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1481286241, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong\n \nИногда выбрать вкус на вечер – весьма сложная задача, если они все нравятся. Поэтому доверьте выбор судьбе. Просто нажмите на паузу и выкладывайте скриншот результата в комментарии.',
         'attachments': [{'type': 'video', 'video': {'id': 456239041, 'owner_id': 340295070,
                                                     'title': 'Доверьте выбор судьбе!', 'duration': 10,
                                                     'description': '', 'date': 1480689626, 'comments': 0,
                                                     'views': 2008, 'width': 800, 'height': 800,
                                                     'photo_130': 'https://pp.userapi.com/c837737/v837737070/c718/7SYD8VOSLeI.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c837737/v837737070/c716/Eb72f1yCHQ4.jpg',
                                                     'photo_800': 'https://pp.userapi.com/c837737/v837737070/c715/dkqNyJWsOVk.jpg',
                                                     'access_key': '055987840e8c176d45', 'repeat': 1,
                                                     'first_frame_320': 'https://pp.userapi.com/c637931/v637931070/13d32/TrSulnJAsss.jpg',
                                                     'first_frame_160': 'https://pp.userapi.com/c637931/v637931070/13d33/eDKqPq6y5u8.jpg',
                                                     'first_frame_130': 'https://pp.userapi.com/c637931/v637931070/13d34/dGs4mbOW9ck.jpg',
                                                     'first_frame_800': 'https://pp.userapi.com/c637931/v637931070/13d31/1ROSNGthWTw.jpg',
                                                     'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 17, 'can_post': 1},
         'likes': {'count': 16, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49103, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1481180446, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nЕсли у вас кончились идеи, что еще подарить друзьям или родственникам, то мы не оставим вас в беде! Смотрите наш новый ролик о том, какие подарки можно сделать своими руками: https://vk.cc/5RZvYm. \nНе забывайте регистрировать коды по ссылке: nysmile.ru и выиграйте призы. \n \n*Общий срок проведения акции — с 01.11.2016 по 10.02.2017, включая период выдачи призов победителям. Подробности на nysmile.ru.',
         'attachments': [{'type': 'video', 'video': {'id': 456239038, 'owner_id': 340295070,
                                                     'title': 'Подарки своими руками', 'duration': 106,
                                                     'description': '', 'date': 1480688658, 'comments': 0,
                                                     'views': 58924, 'width': 1280, 'height': 720,
                                                     'photo_130': 'https://pp.userapi.com/c604330/v604330070/3ca1b/1o7ibPU_a1Y.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c604330/v604330070/3ca19/c6SUPBrjeXs.jpg',
                                                     'photo_800': 'https://pp.userapi.com/c604330/v604330070/3ca18/5c3aFd1g3hg.jpg',
                                                     'access_key': '17aeac19dc3c836853',
                                                     'first_frame_320': 'https://pp.userapi.com/c636125/v636125070/3a13e/aTz0r7EfLPM.jpg',
                                                     'first_frame_160': 'https://pp.userapi.com/c636125/v636125070/3a13f/RIolNn8FFqE.jpg',
                                                     'first_frame_130': 'https://pp.userapi.com/c636125/v636125070/3a140/hrQiuTeyvVk.jpg',
                                                     'first_frame_800': 'https://pp.userapi.com/c636125/v636125070/3a13d/cI0540Ilm2I.jpg',
                                                     'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 261, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 33, 'user_reposted': 0}},
        {'id': 49101, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1481135416, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#футболвкуснеесLays \n\nСегодня в 22:45 (МСК) начнется матч группового этапа Лиги Чемпионов УЕФА «Тоттенхэм» – «ЦСКА»!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239072, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837121/v837121531/143ec/ZyVq1hmf_zM.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837121/v837121531/143ed/8ptspl3Yo_U.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837121/v837121531/143ee/8Dx04y0Lg70.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837121/v837121531/143ef/kzC0_py1UWU.jpg',
                                    'width': 662, 'height': 463, 'text': '', 'date': 1480955673,
                                    'access_key': '11e7c936ad47b11bea'}}, {'type': 'page',
                                                                           'page': {'id': 51214492,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Тоттенхэм - ЦСКА',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1480954171,
                                                                                    'views': 53,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51214492?api_view=062993054ae43d207daf6b167d96b5'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 6, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49094, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1481045457, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#футболвкуснеесLays \n\nСегодня в 22:45 (МСК) начнется следующий матч группового этапа Лиги Чемпионов УЕФА «ПСВ» – «Ростов»!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239071, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837121/v837121531/143dd/ISFaVWI4rQ0.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837121/v837121531/143de/BwCe_cDuGPE.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837121/v837121531/143df/NLUeXWtyC20.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837121/v837121531/143e0/k4Piw4oqaXc.jpg',
                                    'width': 638, 'height': 447, 'text': '', 'date': 1480955358,
                                    'access_key': 'd1c721ce94fe485b3a'}}, {'type': 'page',
                                                                           'page': {'id': 51214378,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'ПСВ - Ростов',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1480952614,
                                                                                    'views': 42,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51214378?api_view=f56b9ecfd0619dff4daf6f36a13b2f'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 8, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49085, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480921231, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n\nПодарок, сделанный своими руками приятнее не только получить на Новый год, но и сделать самим. Если вы не умеете вязать, то мы подготовили для вас подробную инструкцию: https://vk.cc/5RZAus. \n \nНе забывайте регистрировать коды по ссылке: nysmile.ru и выиграйте призы. \n \n*Общий срок проведения акции — с 01.11.2016 по 10.02.2017, включая период выдачи призов победителям. Подробности на nysmile.ru.',
         'attachments': [{'type': 'video',
                          'video': {'id': 456239037, 'owner_id': 340295070, 'title': 'Как связать шарф',
                                    'duration': 96, 'description': '', 'date': 1480688522, 'comments': 0,
                                    'views': 1109, 'width': 1280, 'height': 720,
                                    'photo_130': 'https://pp.userapi.com/c836638/v836638070/fafa/dmevS9IaFU0.jpg',
                                    'photo_320': 'https://pp.userapi.com/c836638/v836638070/faf8/dZXkDv_zqQg.jpg',
                                    'photo_800': 'https://pp.userapi.com/c836638/v836638070/faf7/sRsRDyeu258.jpg',
                                    'access_key': 'aec12b55c6519da500',
                                    'first_frame_320': 'https://pp.userapi.com/c626516/v626516070/368ef/WtGEFZoVpRI.jpg',
                                    'first_frame_160': 'https://pp.userapi.com/c626516/v626516070/368f0/em0biocYB8c.jpg',
                                    'first_frame_130': 'https://pp.userapi.com/c626516/v626516070/368f1/8MuOYLuNvfE.jpg',
                                    'first_frame_800': 'https://pp.userapi.com/c626516/v626516070/368ee/3q-MvRQwe0s.jpg',
                                    'can_add': 1}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 12, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49079, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480780833, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong \nВ 1586 году 3 декабря из Колумбии в Англию был впервые привезен картофель. В связи с этим, советуем вечером отпраздновать парой пачек Lay’s Strong с друзьями такую круглую дату!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239059, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837238/v837238070/1a536/pryPcJ_6Rhg.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837238/v837238070/1a537/eZS4r6V_aKA.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837238/v837238070/1a538/gA7reQaThrg.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837238/v837238070/1a539/RarKf4-wMjY.jpg',
                                    'width': 800, 'height': 800, 'text': '', 'date': 1480613249,
                                    'post_id': 49079, 'access_key': 'd199b5629f99aa9569'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 27, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49078, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480701665, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \n45 лет назад на Марсе появился новый житель – Автоматическая межпланетная станция Марс-3. Шесть месяцев в пути и в пылевую бурю он приземлился между областями Электрида и Фаэтонтия. В течение 1,5 минут после посадки АМС вышла на связь, но через 14,5 секунд трансляция прекратилась. Так до сих пор до конца и не известно, что на самом деле с ней произошло…',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 439413116, 'owner_id': 340295070, 'title': 'giphy.gif',
                                  'size': 1833380, 'ext': 'gif',
                                  'url': 'https://vk.com/doc340295070_439413116?hash=7003b3177703038b52&dl=149081290726f1e57e12062e1924&api=1&no_preview=1',
                                  'date': 1480613102, 'type': 3, 'preview': {'photo': {'sizes': [
                                  {'src': 'https://pp.userapi.com/c812736/u340295070/-3/m_54dfb56d14.jpg',
                                   'width': 130, 'height': 100, 'type': 'm'},
                                  {'src': 'https://pp.userapi.com/c812736/u340295070/-3/s_54dfb56d14.jpg',
                                   'width': 100, 'height': 75, 'type': 's'},
                                  {'src': 'https://pp.userapi.com/c812736/u340295070/-3/x_54dfb56d14.jpg',
                                   'width': 604, 'height': 604, 'type': 'x'},
                                  {'src': 'https://pp.userapi.com/c812736/u340295070/-3/o_54dfb56d14.jpg',
                                   'width': 480, 'height': 480, 'type': 'o'}]}, 'video': {
                                  'src': 'https://vk.com/doc340295070_439413116?hash=7003b3177703038b52&dl=149081290726f1e57e12062e1924&api=1&mp4=1',
                                  'width': 480, 'height': 480, 'file_size': 86266}},
                                  'access_key': 'b819f265fa23f0cde3'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 15, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49063, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480615400, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \nВ следующем году повесть «Этюд в багровых тонах» Артура Конана Дойла ждёт большой юбилей, ведь 1 декабря 1887 года после ряда отказов она была опубликована в журнале Beeton's Christmas Annual. \n \nКстати, через месяц в новогоднюю ночь можно будет посмотреть новый эпизод сериала «Шерлок».",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239056, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837238/v837238070/1a525/3gBBX9k0tGQ.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837238/v837238070/1a526/wr2QE7Ufmb8.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837238/v837238070/1a527/DYcToikSbkQ.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837238/v837238070/1a528/HFp3fgJOJbU.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837238/v837238070/1a529/_zBWPCwcbVU.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1480611307,
                                    'access_key': '10fe4fe82e89fd0f6f'}}, {'type': 'page',
                                                                           'page': {'id': 51206264,
                                                                                    'group_id': 39834333,
                                                                                    'title': 'Этюд в багровых тонах',
                                                                                    'who_can_view': 2,
                                                                                    'who_can_edit': 0,
                                                                                    'edited': 0,
                                                                                    'created': 1480611176,
                                                                                    'views': 42,
                                                                                    'view_url': 'https://m.vk.com/page-39834333_51206264?api_view=2951e0654817e7328daf6c914b97d0'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 17, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49049, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480527011, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \nНовую пачку Lay's разработали специально для идеального перекуса. 40 грамм в эргономичной упаковке подходят для утоления голода в любом удобном месте. \nНовинку ищите на полках магазинов вашего города!",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239043, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837237/v837237070/125ac/TsezTuQNl7I.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837237/v837237070/125ad/jGvdu_fLmBY.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837237/v837237070/125ae/sagpfKTNuf8.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837237/v837237070/125af/qyr6yHQK_jQ.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837237/v837237070/125b0/FXATRBefvjU.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1479911658,
                                    'post_id': 49049, 'access_key': '77c602396d9b89d19c'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 3, 'can_post': 1},
         'likes': {'count': 23, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 3, 'user_reposted': 0}},
        {'id': 49048, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480519696, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#футболвкуснеесLays \nСегодня, 30 ноября, знаменательная дата в истории футбола – первая официальная встреча международных команд. \nВ конце XIX века представители клуба «Куинз Парк» из Глазго предложили, чтобы в сезоне 1872/1873 ведущие английские и шотландские футболисты сыграли в Глазго. И 30 ноября 1872 года эта встреча состоялась, завершившаяся нулевой ничьей. К 1882 году существовало уже четыре футбольные ассоциации: Англии, Шотландии, Уэльса и Ирландии. Этими организациями в том же году был создан Международный совет футбольных ассоциаций для контроля изменений правил игры.',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239055, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837238/v837238070/19e72/GYo7Fy-sufw.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837238/v837238070/19e73/sYu278Qh1WI.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837238/v837238070/19e74/W2wa1Z5EP2k.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837238/v837238070/19e75/0_VEkbbYSGk.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837238/v837238070/19e76/69Aq1ZcSIg0.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1480519695,
                                    'post_id': 49048, 'access_key': 'a2eabca13adc93365a'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 9, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49043, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480434103, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \nБлондинка, хипстеры и Гарик Харламов. Чем закончится эта встреча? Ты решаешь! Выбирай, какую концовку будут показывать во всех телевизорах страны! \n \nhttps://vk.cc/5LBBka',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 439347953, 'owner_id': 340295070, 'title': '5.gif', 'size': 1301225,
                                  'ext': 'gif',
                                  'url': 'https://vk.com/doc340295070_439347953?hash=976d630fe78180a2bb&dl=1490812907d17fb73d6c53b2a779&api=1&no_preview=1',
                                  'date': 1480433990, 'type': 3, 'preview': {'photo': {'sizes': [
                                  {'src': 'https://pp.userapi.com/c812221/u340295070/-3/m_e7d3354368.jpg',
                                   'width': 130, 'height': 87, 'type': 'm'},
                                  {'src': 'https://pp.userapi.com/c812221/u340295070/-3/s_e7d3354368.jpg',
                                   'width': 100, 'height': 67, 'type': 's'},
                                  {'src': 'https://pp.userapi.com/c812221/u340295070/-3/o_e7d3354368.jpg',
                                   'width': 240, 'height': 160, 'type': 'o'}]}, 'video': {
                                  'src': 'https://vk.com/doc340295070_439347953?hash=976d630fe78180a2bb&dl=1490812907d17fb73d6c53b2a779&api=1&mp4=1',
                                  'width': 240, 'height': 160, 'file_size': 86790}},
                                  'access_key': 'c66c35f468f2f4b41d'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 14, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49039, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480345552, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \nПорадуйте себя и своих близких перед Новым годом! \nЗарегистрируйте коды по ссылке: nysmile.ru и выиграйте призы. \n \n*Общий срок проведения акции — с 01.11.2016 по 10.02.2017, включая период выдачи призов победителям. Подробности на nysmile.ru.',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239054, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837238/v837238070/194fd/0xYXiVrPBVc.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837238/v837238070/194fe/yjXd5qKz3PY.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837238/v837238070/194ff/rmBS40HdB_0.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837238/v837238070/19500/ugEkHz0n7bI.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837238/v837238070/19501/JRENkhXamiA.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1480345552,
                                    'post_id': 49039, 'access_key': '9d797e3980c82b6755'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 12, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 49031, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480269765, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \nКаждый раз, когда ты открываешь пачку аппетитных, хрустящих чипсов «Lay's» – ты реально поддерживаешь российское сельское хозяйство. Потому что «Lay's» делаются из 100% российской картошки! \n \nhttps://vk.cc/5LBBka",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239053, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837238/v837238070/190ee/DHD_lInUHcw.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837238/v837238070/190ef/HO46SgJ_zm0.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837238/v837238070/190f0/vpvVkMnivHE.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837238/v837238070/190f1/OWNC20I73Ck.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837238/v837238070/190f2/9gJIu7iSKfA.jpg',
                                    'width': 1100, 'height': 700, 'text': '', 'date': 1480269766,
                                    'post_id': 49031, 'access_key': '535216ee4756b55537'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 5, 'can_post': 1},
         'likes': {'count': 19, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49019, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480168928, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays #Strong \nВечер субботы – драгоценное время. Проведите его вкусно в компании друзей и Lay’s Strong!',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239049, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837238/v837238070/189b7/lVdXxInJTVY.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837238/v837238070/189b8/uuP60HQ8aHY.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837238/v837238070/189b9/bwjqzZ9Lqeo.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837238/v837238070/189ba/K-PgXHlwYsM.jpg',
                                    'width': 800, 'height': 800, 'text': '', 'date': 1480168929,
                                    'post_id': 49019, 'access_key': '9eb51532b3d4e9920f'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 7, 'can_post': 1},
         'likes': {'count': 18, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 49013, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1480013918, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \n100% российская картошка – это как? Покупай «Lay's» – узнаешь! И не забудь собрать свою версию российской картошки в нашем конструкторе! \n \nhttp://potato.lays.ru/constructor/",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239047, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837238/v837238070/18259/AHyWH_9g5X0.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837238/v837238070/1825a/TJqKj_khgRk.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837238/v837238070/1825b/u1h6zW3lsoQ.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837238/v837238070/1825c/db-FqRmWApM.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837238/v837238070/1825d/i-ASajySwBs.jpg',
                                    'width': 1100, 'height': 700, 'text': '', 'date': 1480013918,
                                    'post_id': 49013, 'access_key': '3244a5802b1e6612d0'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 11, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49005, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479919285, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#футболвкуснеесLays \nСегодня в 20:00 (МСК) начнется матч группового этапа Лиги Чемпионов УЕФА «Ростов» – «Бавария»! \nМы решили сравнить эти два настолько непохожих клуба и вот, что получилось: https://vk.cc/5SxMRq.',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239044, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837237/v837237070/125f1/c82d-lPstu4.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837237/v837237070/125f2/_K8Iwz_3Q_c.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837237/v837237070/125f3/6J-fk5xgI6I.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837237/v837237070/125f4/sOR4cozIOkU.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837237/v837237070/125f5/4_vbNGJ4blU.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1479919285,
                                    'post_id': 49005, 'access_key': '143390b67ab21a4e0b'}}, {'type': 'page',
                                                                                             'page': {
                                                                                                 'id': 51185689,
                                                                                                 'group_id': 39834333,
                                                                                                 'title': 'Ростов-Бавария 23.11',
                                                                                                 'who_can_view': 2,
                                                                                                 'who_can_edit': 0,
                                                                                                 'edited': 0,
                                                                                                 'created': 1479919104,
                                                                                                 'views': 49,
                                                                                                 'view_url': 'https://m.vk.com/page-39834333_51185689?api_view=8404898a9b5e44185daf69c7d569b7'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 14, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 49000, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479828447, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#футболвкуснеесLays \nСегодня в 20:00 (МСК) начнется матч группового этапа Лиги Чемпионов УЕФА «ЦСКА» – «Байер»! \nЧто ждать от встречи, смотрите по ссылке: https://vk.cc/5Sg1zh.',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239042, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837237/v837237070/12304/G_NwmhZxuW4.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837237/v837237070/12305/WXkJjPuLfvI.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837237/v837237070/12306/opK7nlIQlXY.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837237/v837237070/12307/eT33wOWCsow.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837237/v837237070/12308/lSdR5As2PY4.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1479828447,
                                    'post_id': 49000, 'access_key': '8325b8425473eb3f47'}}, {'type': 'page',
                                                                                             'page': {
                                                                                                 'id': 51181990,
                                                                                                 'group_id': 39834333,
                                                                                                 'title': 'ЦСКА-Байер 22.11',
                                                                                                 'who_can_view': 2,
                                                                                                 'who_can_edit': 0,
                                                                                                 'edited': 0,
                                                                                                 'created': 1479826968,
                                                                                                 'views': 24,
                                                                                                 'view_url': 'https://m.vk.com/page-39834333_51181990?api_view=3ccacb83f5e8de33ddaf6523f5fa8f'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 9, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 48998, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479817386, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \nВыбери финальную шутку для Гарика Харламова! Смотри историю и решай сам, какую концовку будут показывать во всех телевизорах страны! \n \nhttps://vk.cc/5LBBka',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239041, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837237/v837237070/122cc/2HT1prJir6w.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837237/v837237070/122cd/6m8IxNenPhI.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837237/v837237070/122ce/tV7rpREQ9xI.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837237/v837237070/122cf/GC7wjtFbY_M.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837237/v837237070/122d0/9O6aH-8bsSk.jpg',
                                    'width': 1100, 'height': 700, 'text': '', 'date': 1479817385,
                                    'post_id': 48998, 'access_key': 'd737d64f1119d0dc66'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 19, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 48995, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479751396, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \nХочется перекусить? Lay's специально для тебя выпускает новый размер пачки, который удобно взять с собой и похрустеть в любом удобном месте. \nИщите новинку на полках магазинов вашего города!",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239040, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837237/v837237070/120d2/3f451s9wOoE.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837237/v837237070/120d3/4r8AGp5RFpo.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837237/v837237070/120d4/psO7h-vGDN0.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837237/v837237070/120d5/IO0k4saqNKg.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837237/v837237070/120d6/ypGvqb0B9CQ.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1479745952,
                                    'post_id': 48995, 'access_key': 'c08c242ce5c3313d0e'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 8, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 48993, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479745244, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \nДай пять российской картофелине в честь Всемирного дня приветствий и начни производство чипсов Lay’s всего одним движением пальца!',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 439114633, 'owner_id': 340295070, 'title': 'High five.gif',
                                  'size': 3035490, 'ext': 'gif',
                                  'url': 'https://vk.com/doc340295070_439114633?hash=753018ed35773e7f26&dl=14908129074b744060323949aef9&api=1&no_preview=1',
                                  'date': 1479745630, 'type': 3, 'preview': {'photo': {'sizes': [{
                                  'src': 'https://cs7065.userapi.com/c810338/u340295070/-3/m_036ce12895.jpg',
                                  'width': 130,
                                  'height': 100,
                                  'type': 'm'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c810338/u340295070/-3/s_036ce12895.jpg',
                                      'width': 100,
                                      'height': 75,
                                      'type': 's'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c810338/u340295070/-3/x_036ce12895.jpg',
                                      'width': 604,
                                      'height': 604,
                                      'type': 'x'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c810338/u340295070/-3/y_036ce12895.jpg',
                                      'width': 807,
                                      'height': 807,
                                      'type': 'y'},
                                  {
                                      'src': 'https://cs7065.userapi.com/c810338/u340295070/-3/o_036ce12895.jpg',
                                      'width': 800,
                                      'height': 800,
                                      'type': 'o'}]},
                                  'video': {
                                      'src': 'https://vk.com/doc340295070_439114633?hash=753018ed35773e7f26&dl=14908129074b744060323949aef9&api=1&mp4=1',
                                      'width': 800,
                                      'height': 800,
                                      'file_size': 241269}},
                                  'access_key': 'db60af5b2e3c2b7524'}}], 'post_source': {'type': 'vk'},
         'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 21, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 48985, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479721520, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': 'Словосочетания «новый фильм», «Фёдор Бондарчук» и «инопланетяне» в одном предложении — это как минимум любопытно! А когда в актерской команде такие имена, как Александр Петров, Олег Меньшиков, Ирина Старшенбаум и Риналь Мухаметов, становится еще заманчивее. Сегодня межгалактическая премьера нового трейлера фильма «Притяжение» про пришельцев, приземлившихся в Москве — чем интереснее сюжет, тем больше хочется закусить его чипсами. Не забывайте, что #киновкуснеесLays. И участвуйте в акции «Начни год с улыбки», чтобы получить шанс выиграть сертификаты на показ фильма «Притяжение» и другие ценные призы. \n \n#Притяжение #ИспытайПритяжение',
         'attachments': [{'type': 'video', 'video': {'id': 456239061, 'owner_id': -39834333,
                                                     'title': 'Притяжение - третий трейлер (2017)',
                                                     'duration': 125,
                                                     'description': 'В кино с 26 января 2017\nhttps://sonypictures.ru/prityazhenie/ \n\nО фильме: \n«…Как только что стало известно, сбитый над Москвой \nнеопознанный объект имеет, возможно, внеземное \nпроисхождение. Большая часть столичного Чертанова \nоцеплена, к месту крушения стягиваются \nпредставители силовых структур, решается вопрос об \nэвакуации местных жителей. По словам нашего \nисточника в Минобороны, сейчас специальная комиссия \nпытается вступить в контакт с так называемыми \n«гостями». В эти минуты мы готовим экстренный \nв',
                                                     'date': 1479721520, 'comments': 0, 'views': 59476,
                                                     'photo_130': 'https://pp.userapi.com/c636427/u30801908/video/s_9d3ecb15.jpg',
                                                     'photo_320': 'https://pp.userapi.com/c636427/u30801908/video/l_8c7306c1.jpg',
                                                     'photo_640': 'https://pp.userapi.com/c636427/u30801908/video/y_38b90ac0.jpg',
                                                     'access_key': 'c6ccc3ab3b597c68ae',
                                                     'platform': 'YouTube', 'can_add': 1}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 18, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 2, 'user_reposted': 0}},
        {'id': 48978, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479664010, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \nСамые популярные чипсы в России стали еще роднее! Теперь Lay's делаются из 100% российской картошки. Попробуй этот потрясающий вкус! \n \nhttps://vk.cc/5LBBka",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239039, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837237/v837237070/11db1/Qs7fTeoezzs.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837237/v837237070/11db2/0hte5A1sD68.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837237/v837237070/11db3/AeJGm14nM1Y.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837237/v837237070/11db4/4_E9O9hC9Ho.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837237/v837237070/11db5/P33DiXYSHU4.jpg',
                                    'width': 1100, 'height': 700, 'text': '', 'date': 1479664011,
                                    'post_id': 48978, 'access_key': '2a377d26fc2a375b53'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 18, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 1, 'user_reposted': 0}},
        {'id': 48966, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479576382, 'marked_as_ads': 0,
         'post_type': 'post', 'text': '#каждыйденьвкуснеесLays #Strong \nКакие Lay’s Strong вкуснее?',
         'attachments': [{'type': 'doc',
                          'doc': {'id': 439060328, 'owner_id': 340295070, 'title': 'Strong.gif',
                                  'size': 2768136, 'ext': 'gif',
                                  'url': 'https://vk.com/doc340295070_439060328?hash=fca590fa206e04c852&dl=14908129072525d50d2f86e80ef7&api=1&no_preview=1',
                                  'date': 1479576245, 'type': 3, 'preview': {'photo': {'sizes': [
                                  {'src': 'https://pp.userapi.com/c810626/u340295070/-3/m_6534d1d0d1.jpg',
                                   'width': 130, 'height': 100, 'type': 'm'},
                                  {'src': 'https://pp.userapi.com/c810626/u340295070/-3/s_6534d1d0d1.jpg',
                                   'width': 100, 'height': 75, 'type': 's'},
                                  {'src': 'https://pp.userapi.com/c810626/u340295070/-3/x_6534d1d0d1.jpg',
                                   'width': 604, 'height': 604, 'type': 'x'},
                                  {'src': 'https://pp.userapi.com/c810626/u340295070/-3/y_6534d1d0d1.jpg',
                                   'width': 807, 'height': 807, 'type': 'y'},
                                  {'src': 'https://pp.userapi.com/c810626/u340295070/-3/o_6534d1d0d1.jpg',
                                   'width': 800, 'height': 800, 'type': 'o'}]}, 'video': {
                                  'src': 'https://vk.com/doc340295070_439060328?hash=fca590fa206e04c852&dl=14908129072525d50d2f86e80ef7&api=1&mp4=1',
                                  'width': 800, 'height': 800, 'file_size': 500292}},
                                  'access_key': 'e1bd69b361d455dbb6'}}, {'type': 'poll',
                                                                         'poll': {'id': 245194365,
                                                                                  'owner_id': -39834333,
                                                                                  'created': 1479576383,
                                                                                  'question': 'Какие Lay’s Strong вкуснее?',
                                                                                  'votes': 467,
                                                                                  'answer_id': 0,
                                                                                  'answers': [
                                                                                      {'id': 819332864,
                                                                                       'text': '«Холодец с хреном»',
                                                                                       'votes': 97,
                                                                                       'rate': 20.77},
                                                                                      {'id': 819332865,
                                                                                       'text': '«Охотничьи колбаски»',
                                                                                       'votes': 210,
                                                                                       'rate': 44.97},
                                                                                      {'id': 819332866,
                                                                                       'text': '«Королевская креветка»',
                                                                                       'votes': 160,
                                                                                       'rate': 34.26}],
                                                                                  'anonymous': 0}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 12, 'can_post': 1},
         'likes': {'count': 12, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 48956, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479478603, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': "#каждыйденьвкуснеесLays \n100% российская картошка – как ты себе это представляешь? Покупай «Lay's» из российской картошки – и собери свою в нашем конструкторе! \n \nhttp://potato.lays.ru/constructor/",
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239035, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837237/v837237070/11788/UhPsU8hm9Uk.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837237/v837237070/11789/4U5wHwN8lRw.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837237/v837237070/1178a/rI8r6Cld7Xs.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837237/v837237070/1178b/ZOnDDtE2-W0.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837237/v837237070/1178c/cnuxRCoo_vQ.jpg',
                                    'width': 1100, 'height': 700, 'text': '', 'date': 1479478604,
                                    'post_id': 48956, 'access_key': 'cf5c60223866c5878a'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 6, 'can_post': 1},
         'likes': {'count': 14, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}},
        {'id': 48954, 'from_id': -39834333, 'owner_id': -39834333, 'date': 1479391421, 'marked_as_ads': 0,
         'post_type': 'post',
         'text': '#каждыйденьвкуснеесLays \nФанаты мира Гарри Поттера, все уже спланировали вечер? Если нет, то бегом за билетами, ведь сегодня во всех кинотеатрах стартует фильм «Фантастические твари и места их обитания». Премьера – долгожданная, а значит надо хорошо подготовиться! \nЧитайте по ссылке о книге, ставшей основой для кинокартины, и самом фильме: https://vk.cc/5QVg8P.',
         'attachments': [{'type': 'photo',
                          'photo': {'id': 456239034, 'album_id': -7, 'owner_id': -39834333, 'user_id': 100,
                                    'photo_75': 'https://pp.userapi.com/c837238/v837238070/165d8/UTMiBQL6ZGc.jpg',
                                    'photo_130': 'https://pp.userapi.com/c837238/v837238070/165d9/_gqkHP24MEk.jpg',
                                    'photo_604': 'https://pp.userapi.com/c837238/v837238070/165da/G3A6NNQ1SLE.jpg',
                                    'photo_807': 'https://pp.userapi.com/c837238/v837238070/165db/yZBzyAJbvHc.jpg',
                                    'photo_1280': 'https://pp.userapi.com/c837238/v837238070/165dc/gjz2DqO2FJ8.jpg',
                                    'width': 1000, 'height': 700, 'text': '', 'date': 1479391420,
                                    'post_id': 48954, 'access_key': '6481db3bea024e992b'}}, {'type': 'page',
                                                                                             'page': {
                                                                                                 'id': 51167862,
                                                                                                 'group_id': 39834333,
                                                                                                 'title': '«Фантастические твари и места их обитания»',
                                                                                                 'who_can_view': 2,
                                                                                                 'who_can_edit': 0,
                                                                                                 'edited': 0,
                                                                                                 'created': 1479391116,
                                                                                                 'views': 45,
                                                                                                 'view_url': 'https://m.vk.com/page-39834333_51167862?api_view=e217e1c98fcaad9e3daf68f151544f'}}],
         'post_source': {'type': 'vk'}, 'comments': {'count': 0, 'can_post': 1},
         'likes': {'count': 13, 'user_likes': 0, 'can_like': 1, 'can_publish': 1},
         'reposts': {'count': 0, 'user_reposted': 0}}
    ]}
    groups = [{'id': 1331201, 'name': 'Чемпионат | Championat.com', 'screen_name': 'championat', 'is_closed': 0,
               'type': 'page', 'is_admin': 0, 'is_member': 0, 'activity': 'СМИ', 'age_limits': 1,
               'description': 'Официальная группа Чемпионат.com', 'members_count': 834040,
               'site': 'www.championat.com',
               'status': '', 'verified': 1, 'wiki_page': 'Биатлон. Расписание на сезон',
               'photo_50': 'https://pp.userapi.com/c622327/v622327984/4a0be/9X1BixqWf1U.jpg',
               'photo_100': 'https://pp.userapi.com/c622327/v622327984/4a0bd/JqT7gigpYe0.jpg',
               'photo_200': 'https://pp.userapi.com/c622327/v622327984/4a0bc/tFMHaIZPbCE.jpg'}]
    my_worker = DB_worker()
    my_worker.write_group_to_base(groups[0])
    my_engine = sqlalchemy.create_engine(database_full_name)
    session = Session(bind=my_engine, autocommit=True)
    print(session.query(Groups).first())
    # Post1= Posts(attr1="ma1")
    # print()
    # print(session.query(Posts).first())
    """
        db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=engine))
        Base.query = db_session.query_property()
        # connection.execute("commit")
        Groups.Add_to_base(1132, "link", connection)
        print()
    """
