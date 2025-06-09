from project import check_creds, uploader, check_folder
from unittest.mock import Mock, patch, MagicMock
import pytest
import os



@patch("project.os.path.exists")
@patch("project.Credentials.from_authorized_user_file")
def test_check_creds(fake_creds,fake_path_check): 

    def fake_path(path):
        if path == "token.json" or path == "client_secrets.json":
            return True
        return False
    fake_path_check.side_effect = fake_path

    fake_creds1 = MagicMock()
    fake_creds1.valid = True
    fake_creds.return_value = fake_creds1

    creds = check_creds()

    assert creds.valid

@patch("project.build")  # replace googles api build function with a a mock

 # fake_build is automatticaly passed by @patch and tmp_path is pasrt of pytest for fake file path
def test_uploader(fake_build, tmp_path):

# create fake creds
    creds = Mock()  

    # create fake video
    fake_video = tmp_path.joinpath("test_video.mp4")
    fake_video.write_text("fake text")
    
    # create fake youtube api
    fake_service = Mock()
    fake_videos = Mock()
    fake_insert = Mock()
    fake_execute = Mock(return_value={"id": "fake_id"}) 

    fake_insert.execute = fake_execute
    fake_videos.insert = Mock(return_value = fake_insert)
    fake_service.videos = Mock(return_value = fake_videos)
    fake_build.return_value = fake_service
    
    # run uploader
    uploader(creds, str(tmp_path), "test description")

    # Asserts 
    fake_videos.insert.assert_called() # .assert_called is part of unittest.mock.Mock
    fake_execute.assert_called()

def test_check_folder(tmp_path):
    mp4_file = tmp_path / "video.mp4"
    mp4_file.write_text("fake text")

    assert check_folder(str(tmp_path)) == True

    mp4_file.unlink()
    txt_file = tmp_path / "file.txt"
    txt_file.write_text("fake text")

    assert check_folder(str(tmp_path)) == False

    no_folder = tmp_path / "no folder"
    assert check_folder(str(no_folder)) == False