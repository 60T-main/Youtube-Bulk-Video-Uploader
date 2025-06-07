from project import check_creds, uploader
from unittest.mock import Mock, patch
import pytest
import os

def test_check_creds(): 
    creds = check_creds()
    assert creds != None
    assert creds.valid or creds.expired


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