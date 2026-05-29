"""Tests for cut_clips.py — run from the helpers/ dir:

    python3 -m unittest test_cut_clips -v
"""

import unittest

import cut_clips as cc


class TestParseRanges(unittest.TestCase):
    def test_none_returns_all_indices(self):
        self.assertEqual(cc.parse_ranges(None, 4), [0, 1, 2, 3])

    def test_comma_list_parsed_in_order(self):
        self.assertEqual(cc.parse_ranges("0,2,5", 6), [0, 2, 5])

    def test_whitespace_tolerated(self):
        self.assertEqual(cc.parse_ranges(" 0 , 2 ,5 ", 6), [0, 2, 5])

    def test_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            cc.parse_ranges("0,9", 3)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            cc.parse_ranges("-1", 3)

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            cc.parse_ranges("0,abc", 3)


class TestKebab(unittest.TestCase):
    def test_spaces_and_punctuation_collapse(self):
        self.assertEqual(cc.kebab("My Great Segment!"), "my-great-segment")

    def test_mixed_separators_normalized(self):
        self.assertEqual(cc.kebab("Already-kebab_case"), "already-kebab-case")

    def test_leading_trailing_stripped(self):
        self.assertEqual(cc.kebab("  --Hello--  "), "hello")

    def test_empty_stays_empty(self):
        self.assertEqual(cc.kebab(""), "")


class TestSanitizeBeat(unittest.TestCase):
    def test_none_is_empty(self):
        self.assertEqual(cc.sanitize_beat(None), "")

    def test_empty_is_empty(self):
        self.assertEqual(cc.sanitize_beat(""), "")

    def test_uppercase_token_preserved(self):
        self.assertEqual(cc.sanitize_beat("HOOK"), "HOOK")

    def test_case_preserved_spaces_hyphenated(self):
        self.assertEqual(cc.sanitize_beat("Call To Action"), "Call-To-Action")

    def test_unsafe_chars_replaced(self):
        self.assertEqual(cc.sanitize_beat("intro/outro?"), "intro-outro")


class TestClipFilename(unittest.TestCase):
    def test_with_beat_zero_padded(self):
        self.assertEqual(
            cc.clip_filename(0, "HOOK", "C0103"), "seg_00_HOOK_C0103.mov"
        )

    def test_double_digit_index(self):
        self.assertEqual(
            cc.clip_filename(12, "SOLUTION", "C0108"),
            "seg_12_SOLUTION_C0108.mov",
        )

    def test_no_beat_omits_segment(self):
        self.assertEqual(cc.clip_filename(3, None, "C0108"), "seg_03_C0108.mov")

    def test_empty_beat_omits_segment(self):
        self.assertEqual(cc.clip_filename(3, "", "C0108"), "seg_03_C0108.mov")

    def test_beat_with_spaces_sanitized(self):
        self.assertEqual(
            cc.clip_filename(3, "Call To Action", "C0103"),
            "seg_03_Call-To-Action_C0103.mov",
        )

    def test_source_sanitized_not_lowercased(self):
        self.assertEqual(
            cc.clip_filename(1, "HOOK", "Clip 02"), "seg_01_HOOK_Clip-02.mov"
        )


class TestClampWindow(unittest.TestCase):
    def test_normal_handles_applied_both_sides(self):
        self.assertEqual(cc.clamp_window(2.42, 6.85, 1.0, 43.0), (1.42, 7.85))

    def test_clamped_at_zero(self):
        self.assertEqual(cc.clamp_window(0.5, 6.85, 1.0, 43.0), (0.0, 7.85))

    def test_clamped_at_source_duration(self):
        self.assertEqual(cc.clamp_window(2.0, 42.5, 1.0, 43.0), (1.0, 43.0))

    def test_zero_handles_is_exact(self):
        self.assertEqual(cc.clamp_window(2.42, 6.85, 0.0, 43.0), (2.42, 6.85))

    def test_rounded_to_milliseconds(self):
        self.assertEqual(
            cc.clamp_window(2.4239, 6.8512, 1.0, 43.0), (1.424, 7.851)
        )

    def test_start_not_before_end_raises(self):
        with self.assertRaises(ValueError):
            cc.clamp_window(6.0, 6.0, 1.0, 43.0)

    def test_nonpositive_source_duration_raises(self):
        with self.assertRaises(ValueError):
            cc.clamp_window(2.0, 6.0, 1.0, 0.0)

    def test_negative_handles_raises(self):
        with self.assertRaises(ValueError):
            cc.clamp_window(2.0, 6.0, -0.5, 43.0)


class TestClipHash(unittest.TestCase):
    def test_deterministic(self):
        a = cc.clip_hash("/a/b.mov", 1.0, 5.0, "prores")
        b = cc.clip_hash("/a/b.mov", 1.0, 5.0, "prores")
        self.assertEqual(a, b)

    def test_changes_with_codec(self):
        self.assertNotEqual(
            cc.clip_hash("/a/b.mov", 1.0, 5.0, "prores"),
            cc.clip_hash("/a/b.mov", 1.0, 5.0, "h264"),
        )

    def test_changes_with_window(self):
        self.assertNotEqual(
            cc.clip_hash("/a/b.mov", 1.0, 5.0, "prores"),
            cc.clip_hash("/a/b.mov", 1.0, 5.5, "prores"),
        )

    def test_changes_with_source(self):
        self.assertNotEqual(
            cc.clip_hash("/a/b.mov", 1.0, 5.0, "prores"),
            cc.clip_hash("/a/c.mov", 1.0, 5.0, "prores"),
        )


class TestFfmpegCmd(unittest.TestCase):
    def test_prores_exact_argv(self):
        self.assertEqual(
            cc.ffmpeg_cmd("/src.mov", 1.0, 5.0, "prores", "/out.mov"),
            [
                "ffmpeg", "-y", "-i", "/src.mov",
                "-ss", "1.000", "-to", "5.000",
                "-c:v", "prores_ks", "-profile:v", "3",
                "-pix_fmt", "yuv422p10le", "-c:a", "pcm_s16le",
                "-map", "0:v:0", "-map", "0:a:0?", "/out.mov",
            ],
        )

    def test_h264_exact_argv(self):
        self.assertEqual(
            cc.ffmpeg_cmd("/src.mov", 1.0, 5.0, "h264", "/out.mov"),
            [
                "ffmpeg", "-y", "-i", "/src.mov",
                "-ss", "1.000", "-to", "5.000",
                "-c:v", "libx264", "-preset", "slow", "-crf", "14",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                "-movflags", "+faststart",
                "-map", "0:v:0", "-map", "0:a:0?", "/out.mov",
            ],
        )

    def test_seek_is_frame_accurate_after_input(self):
        # -ss/-to AFTER -i <src> = decode-from-zero accurate seek.
        cmd = cc.ffmpeg_cmd("/src.mov", 1.0, 5.0, "prores", "/out.mov")
        self.assertLess(cmd.index("-i"), cmd.index("-ss"))
        self.assertEqual(cmd[cmd.index("-i") + 1], "/src.mov")
        self.assertLess(cmd.index("/src.mov"), cmd.index("-ss"))

    def test_no_audio_fade(self):
        cmd = cc.ffmpeg_cmd("/src.mov", 1.0, 5.0, "prores", "/out.mov")
        self.assertNotIn("-af", cmd)
        self.assertFalse(any("afade" in tok for tok in cmd))

    def test_no_reframe_crop_or_scale(self):
        cmd = cc.ffmpeg_cmd("/src.mov", 1.0, 5.0, "prores", "/out.mov")
        self.assertNotIn("-vf", cmd)
        self.assertFalse(any("crop" in tok or "scale" in tok for tok in cmd))

    def test_seconds_formatted_to_milliseconds(self):
        cmd = cc.ffmpeg_cmd("/src.mov", 1.4239, 7.8512, "prores", "/o.mov")
        self.assertIn("1.424", cmd)
        self.assertIn("7.851", cmd)

    def test_unknown_codec_raises(self):
        with self.assertRaises(ValueError):
            cc.ffmpeg_cmd("/src.mov", 1.0, 5.0, "av1", "/out.mov")


class TestParseProbeDuration(unittest.TestCase):
    def test_uses_format_duration(self):
        probe = {"format": {"duration": "43.04"}, "streams": []}
        self.assertEqual(cc.parse_probe_duration(probe), 43.04)

    def test_falls_back_to_video_stream_duration(self):
        probe = {
            "format": {},
            "streams": [
                {"codec_type": "audio", "duration": "10.0"},
                {"codec_type": "video", "duration": "42.5"},
            ],
        }
        self.assertEqual(cc.parse_probe_duration(probe), 42.5)

    def test_missing_duration_raises(self):
        with self.assertRaises(ValueError):
            cc.parse_probe_duration({"format": {}, "streams": []})


class TestShouldSkip(unittest.TestCase):
    def test_skip_when_file_exists_and_hash_matches_and_ok(self):
        prev = {"hash": "abc", "status": "ok"}
        self.assertTrue(cc.should_skip(prev, "abc", True))

    def test_no_skip_when_file_missing(self):
        prev = {"hash": "abc", "status": "ok"}
        self.assertFalse(cc.should_skip(prev, "abc", False))

    def test_no_skip_when_hash_differs(self):
        prev = {"hash": "abc", "status": "ok"}
        self.assertFalse(cc.should_skip(prev, "xyz", True))

    def test_no_skip_when_prev_failed(self):
        prev = {"hash": "abc", "status": "failed"}
        self.assertFalse(cc.should_skip(prev, "abc", True))

    def test_no_skip_when_no_prev_entry(self):
        self.assertFalse(cc.should_skip(None, "abc", True))


class TestBuildClipEntry(unittest.TestCase):
    def test_composes_window_filename_hash(self):
        rng = {
            "source": "C0103", "start": 2.42, "end": 6.85,
            "beat": "HOOK", "quote": "the hook line",
        }
        e = cc.build_clip_entry(0, rng, "/abs/C0103.MP4", 43.0, 1.0, "prores")
        self.assertEqual(e["index"], 0)
        self.assertEqual(e["filename"], "seg_00_HOOK_C0103.mov")
        self.assertEqual(e["source"], "C0103")
        self.assertEqual(e["src_path"], "/abs/C0103.MP4")
        self.assertEqual(e["start"], 2.42)
        self.assertEqual(e["end"], 6.85)
        self.assertEqual(e["handle_in"], 1.42)
        self.assertEqual(e["handle_out"], 7.85)
        self.assertEqual(e["beat"], "HOOK")
        self.assertEqual(e["quote"], "the hook line")
        self.assertEqual(
            e["hash"], cc.clip_hash("/abs/C0103.MP4", 1.42, 7.85, "prores")
        )
        self.assertEqual(e["status"], "pending")
        self.assertIsNone(e["bytes"])
        self.assertIsNone(e["cc_asset_urn"])

    def test_missing_beat_and_quote_default(self):
        rng = {"source": "C0108", "start": 10.0, "end": 20.0}
        e = cc.build_clip_entry(2, rng, "/abs/C0108.MP4", 60.0, 1.0, "prores")
        self.assertEqual(e["filename"], "seg_02_C0108.mov")
        self.assertEqual(e["beat"], "")
        self.assertEqual(e["quote"], "")


class TestResolveSource(unittest.TestCase):
    def test_returns_mapped_absolute_path(self):
        edl = {"sources": {"C0103": "/abs/C0103.MP4"}}
        self.assertEqual(cc.resolve_source(edl, "C0103"), "/abs/C0103.MP4")

    def test_missing_key_raises_with_name(self):
        edl = {"sources": {"C0103": "/abs/C0103.MP4"}}
        with self.assertRaises(ValueError) as ctx:
            cc.resolve_source(edl, "C9999")
        self.assertIn("C9999", str(ctx.exception))

    def test_no_sources_block_raises(self):
        with self.assertRaises(ValueError):
            cc.resolve_source({}, "C0103")


if __name__ == "__main__":
    unittest.main()
