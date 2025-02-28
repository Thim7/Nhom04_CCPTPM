import requests
import json
from type import *
import pytest
import random

class TestCreateProject:

    @pytest.mark.skip
    def get_all_projects(self):
        resp = requests.get(URL_LIST_PROJECTS)
        json_data = json.loads(resp.text)
        return json_data['_items']

    @pytest.mark.skip
    def delete_all_projects(self):
        resp = requests.get(URL_LIST_PROJECTS)
        json_data = json.loads(resp.text)
        _items = json_data['_items']
        ids = [x['_id'] for x in _items]
        print(f'------ DELETE {len(ids)} projects')
        for idx in ids:
            self.delete_project(idx)

    @pytest.mark.skip
    def delete_project(self, project_id):
        try:
            requests.delete(URL_DELETE_PROJECT + str(project_id))
            print(f"DEL PROJECT {project_id} SUCCESSFULLY")
        except Exception as e:
            print(f"DEL PROJECT ERROR: {e}")


    @pytest.mark.skip
    def create_project(self, video: str) -> json:
        with open(video, 'rb') as f:
            buffer = f.read()
        resp = requests.post(
            url=URL_CREATE_PROJECT,
            files={
                'file': (str(random.random()) + '.mp4', buffer, 'video/mp4')
            }
        )
        return json.loads(resp.text)

    def upload_project(self, path):
        """
            `Test activity diagram: CREATE PROJECT`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Kiểm tra thông tin project
            3. Xóa project
        """
        # tạo project
        resp = self.create_project(path)
        _id = resp['_id']
        print(f'1. created {_id}')
                
        # không xóa project
        #self.delete_project(_id)
        #print(f'3. deleted ok')

    def assert_data_by_ordering(self, resp, path):
        if 'p-01.mp4' in path:
            assert resp['metadata']['codec_name'] == 'h264'
            assert resp['metadata']['width'] == 848
            assert resp['metadata']['height'] == 480
            assert resp['metadata']['r_frame_rate'] == '30/1'
            assert resp['metadata']['bit_rate'] == 1467581
            assert resp['metadata']['nb_frames'] == 1117
            assert abs(resp['metadata']['duration'] - 37.233333) <= 1e-3
            assert resp['metadata']['size'] == 8037827
        elif 'p-02.mp4' in path:
            assert resp['metadata']['codec_name'] == 'h264'
            assert resp['metadata']['width'] == 480
            assert resp['metadata']['height'] == 658
            assert resp['metadata']['r_frame_rate'] == '5/1'
            assert resp['metadata']['bit_rate'] == 1223672
            assert resp['metadata']['nb_frames'] == 12
            assert abs(resp['metadata']['duration'] - 2.2) <= 1e-3
            assert resp['metadata']['size'] == 337454
        elif 'p-03.mp4' in path:
            assert resp['metadata']['codec_name'] == 'h264'
            assert resp['metadata']['width'] == 480
            assert resp['metadata']['height'] == 618
            assert resp['metadata']['r_frame_rate'] == '10/1'
            assert resp['metadata']['bit_rate'] == 1058518
            assert resp['metadata']['nb_frames'] == 24
            assert abs(resp['metadata']['duration'] - 2.300977) <= 1e-3
            assert resp['metadata']['size'] == 305414
        elif 'p-04.mp4' in path:
            assert resp['metadata']['codec_name'] == 'h264'
            assert resp['metadata']['width'] == 372
            assert resp['metadata']['height'] == 480
            assert resp['metadata']['r_frame_rate'] == '133/12'
            assert resp['metadata']['bit_rate'] == 670481
            assert resp['metadata']['nb_frames'] == 24
            assert abs(resp['metadata']['duration'] - 2.07601) <= 1e-3
            assert resp['metadata']['size'] == 174945
        elif 'p-05.mp4' in path:
            assert resp['metadata']['codec_name'] == 'h264'
            assert resp['metadata']['width'] == 480
            assert resp['metadata']['height'] == 574
            assert resp['metadata']['r_frame_rate'] == '31/4'
            assert resp['metadata']['bit_rate'] == 1459549
            assert resp['metadata']['nb_frames'] == 13
            assert abs(resp['metadata']['duration'] - 1.549017) <= 1e-3
            assert resp['metadata']['size'] == 283460
        else:
            raise Exception('unkown path ' + path)


    def test_01(self):
        # xóa toàn bộ project trước
        self.delete_all_projects()

        # upload 3 video
        input_data = [
            'test_data/p-01.mp4',
            'test_data/p-02.mp4',
            'test_data/p-02.mp4'
        ]

        for path in input_data:
            self.upload_project(path)

        import time
        time.sleep(1)

        projects = self.get_all_projects()

        for i, path in enumerate(input_data):
            self.assert_data_by_ordering(projects[i], path)

        assert len(projects) == len(input_data)

        # xóa toàn bộ project test
        self.delete_all_projects()
    
    def test_02(self):
        # xóa toàn bộ project trước
        self.delete_all_projects()

        # upload 3 video
        input_data = [
            'test_data/p-03.mp4',
            'test_data/p-02.mp4',
            'test_data/p-03.mp4'
        ]

        for path in input_data:
            self.upload_project(path)

        import time
        time.sleep(1)


        projects = self.get_all_projects()

        for i, path in enumerate(input_data):
            self.assert_data_by_ordering(projects[i], path)

        # xóa toàn bộ project test
        self.delete_all_projects()

    def test_03(self):
        # xóa toàn bộ project trước
        self.delete_all_projects()

        # upload 3 video
        input_data = [
            'test_data/p-01.mp4',
            'test_data/p-02.mp4',
            'test_data/p-03.mp4',
            'test_data/p-04.mp4',
            'test_data/p-05.mp4',
        ]

        for path in input_data:
            self.upload_project(path)

        import time
        time.sleep(60)

        
        projects = self.get_all_projects()

        for i, path in enumerate(input_data):
            self.assert_data_by_ordering(projects[i], path)

        # xóa toàn bộ project test
        self.delete_all_projects()
