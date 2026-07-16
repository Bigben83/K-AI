import unittest
from unittest import mock

import bridge


class ConversationHistoryTests(unittest.TestCase):
    def test_build_conversation_context_truncates_to_recent_turns(self):
        history = [
            {"prompt": "first prompt", "response": "first response"},
            {"prompt": "second prompt", "response": "second response"},
            {"prompt": "third prompt", "response": "third response"},
        ]

        context = bridge._build_conversation_context(history, max_turns=2)

        self.assertIn("Previous user: second prompt", context)
        self.assertIn("Previous user: third prompt", context)
        self.assertNotIn("Previous user: first prompt", context)

    def test_build_conversation_context_is_empty_when_history_is_empty(self):
        self.assertEqual(bridge._build_conversation_context([]), "")

    def test_reset_conversation_history_clears_existing_turns(self):
        bridge.conversation_history = [{"prompt": "hello", "response": "hi"}]

        bridge._reset_conversation_history()

        self.assertEqual(bridge.conversation_history, [])

    def test_ensure_alive_recovers_when_browser_check_raises(self):
        bridge.driver = object()

        with mock.patch.object(bridge, "is_alive", side_effect=RuntimeError("session not created")), \
             mock.patch.object(bridge, "start_browser") as start_browser_mock:
            bridge.ensure_alive()

        start_browser_mock.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
