import unittest
from unittest.mock import patch, MagicMock
from youtube_downloader.transcoder import parse_fps, analyze_video, transcode_video

class TestTranscoder(unittest.TestCase):
    def test_parse_fps(self):
        self.assertEqual(parse_fps("30/1"), 30.0)
        self.assertEqual(parse_fps("24000/1001"), 24000/1001)
        self.assertEqual(parse_fps("25"), 25.0)
        self.assertEqual(parse_fps("0/0"), 0.0)
        self.assertEqual(parse_fps(None), 0.0)
        self.assertEqual(parse_fps("invalid"), 0.0)

    @patch('youtube_downloader.transcoder.get_video_info')
    def test_analyze_video(self, mock_get_info):
        # Mock typical ffprobe output for a high-res video
        mock_get_info.return_value = {
            'format': {
                'duration': '123.45',
                'format_name': 'matroska,webm'
            },
            'streams': [
                {
                    'codec_type': 'video',
                    'width': 1920,
                    'height': 1080,
                    'codec_name': 'vp9',
                    'r_frame_rate': '60/1'
                },
                {
                    'codec_type': 'audio',
                    'codec_name': 'opus'
                }
            ]
        }
        
        info = analyze_video("dummy_path.webm")
        self.assertEqual(info['width'], 1920)
        self.assertEqual(info['height'], 1080)
        self.assertEqual(info['fps'], 60.0)
        self.assertEqual(info['video_codec'], 'vp9')
        self.assertEqual(info['audio_codec'], 'opus')
        self.assertEqual(info['duration'], 123.45)
        self.assertEqual(info['format'], 'matroska,webm')

    @patch('subprocess.Popen')
    def test_transcode_video_h264(self, mock_popen):
        # Mock subprocess.Popen for transcoding progress
        mock_proc = MagicMock()
        mock_proc.stdout.readline.side_effect = [
            "frame=1\n",
            "out_time_us=5000000\n",
            ""
        ]
        mock_proc.wait.return_value = 0
        mock_proc.returncode = 0
        mock_popen.return_value = mock_proc

        source_info = {
            'width': 1280,
            'height': 720,
            'fps': 30.0,
            'duration': 10.0,
            'video_codec': 'vp9',
            'audio_codec': 'opus'
        }

        progress_calls = []
        def progress_callback(pct):
            progress_calls.append(pct)

        transcode_video(
            input_path="input.webm",
            output_path="output.mp4",
            target_format="h264",
            source_info=source_info,
            progress_callback=progress_callback
        )

        # Ensure ffmpeg was called
        mock_popen.assert_called_once()
        args = mock_popen.call_args[0][0]
        self.assertIn("ffmpeg", args)
        self.assertIn("libx264", args)
        self.assertIn("aac", args)
        self.assertIn("output.mp4", args)
        
        # Verify progress callback was invoked (5.0s out of 10.0s = 50%)
        self.assertIn(50.0, progress_calls)

    @patch('subprocess.Popen')
    def test_transcode_video_prores_with_fps_downsampling(self, mock_popen):
        mock_proc = MagicMock()
        mock_proc.stdout.readline.side_effect = [""]
        mock_proc.wait.return_value = 0
        mock_proc.returncode = 0
        mock_popen.return_value = mock_proc

        source_info = {
            'width': 1920,
            'height': 1080,
            'fps': 60.0,  # exceeds 30.5 -> should apply fps=fps=30 filter
            'duration': 10.0,
            'video_codec': 'vp9',
            'audio_codec': 'opus'
        }

        transcode_video(
            input_path="input.webm",
            output_path="output.mov",
            target_format="prores",
            source_info=source_info
        )

        args = mock_popen.call_args[0][0]
        self.assertIn("prores_ks", args)
        self.assertIn("pcm_s16le", args)
        self.assertIn("-vf", args)
        self.assertIn("fps=fps=30", args)
        self.assertIn("output.mov", args)

if __name__ == '__main__':
    unittest.main()
