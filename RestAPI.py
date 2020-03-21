from DatabaseManager import DatabaseManager
from flask_restful import Resource, reqparse
from flask import jsonify, request

db = DatabaseManager('ddol.site', 'root', 'Qwer!234!@#$', 'uptown_rumor_temp')

class Post(Resource):
    # 글쓰기
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('region_code', type=int)

        args = parser.parse_args()
        title = args['title']
        content = args['content']
        region_code = args['region_code']

        sql = f"insert into post (title, content, region_code) values ('{title}', '{content}', '{region_code}')"

        db.curs.execute(sql)
        db.conn.commit()

        result = {"status": 200, "message":"ok"}
        return jsonify(result)

    # 글조회
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('idx', type=int)
        parser.add_argument('region_code', type=int)
        parser.add_argument('startIndex', type=int)

        args = parser.parse_args()
        idx = args['idx']
        region_code = args['region_code']
        startIndex = args['startIndex']

        # 조회 시 지역코드가 있으면 지역 내 게시물 리스트 조회, 없으면 단일 게시물 조회
        if region_code is not None:
            sql = f"select * from post where region_code = ('{region_code}')"
        else:
            sql = f"select * from post where idx = ('{idx}')"

        db.curs.execute(sql)
        row_headers = [x[0] for x in db.curs.description]  # this will extract row headers

        db.conn.commit()
        rows = db.curs.fetchall()

        post_data = []
        for result in rows:
            post_data.append(dict(zip(row_headers, result)))

        result = {"status": 200, "message":"ok", "post":post_data}
        return jsonify(result)


    # 글수정
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('idx', type=int)
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)

        args = parser.parse_args()

        idx = args['idx']
        title = args['title']
        content = args['content']

        sql = f"update post set title = '{title}', content = '{content}' where idx = '{idx}'"
        db.curs.execute(sql)
        db.conn.commit()
        status = 1

        result = {"status": 200, "message":"ok"}
        return jsonify(result)

    # 글삭제
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('idx', type=int)

        args = parser.parse_args()

        idx = args['idx']

        sql = f"delete from post where idx = ('{idx}')"
        db.curs.execute(sql)
        db.conn.commit()
        row = db.curs.fetchone()
        result = {'status':1, "message":row}
        return jsonify(result)