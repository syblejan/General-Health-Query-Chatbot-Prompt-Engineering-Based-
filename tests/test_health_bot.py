import io
import json
import unittest
from unittest.mock import Mock, patch
from health_bot import ChatError, HealthBot, MistralClient, SYSTEM_PROMPT


class ConversationTests(unittest.TestCase):
    def setUp(self):
        self.client = Mock()
        self.client.complete.return_value = "General educational response."
        self.bot = HealthBot(self.client)

    def test_follow_up_receives_history_and_system(self):
        self.bot.ask("Explain hydration.")
        self.bot.ask("Explain that more simply.")
        sent = self.client.complete.call_args.args[0]
        self.assertEqual([m['role'] for m in sent], ['system', 'user', 'assistant', 'user'])
        self.assertEqual(sent[0]['content'], SYSTEM_PROMPT)
        self.assertEqual(sent[1]['content'], 'Explain hydration.')

    def test_history_has_six_complete_turns(self):
        for i in range(10):
            self.bot.ask(str(i))
        self.bot.ask("next")
        sent = self.client.complete.call_args.args[0]
        self.assertEqual(len(sent), 14)
        self.assertEqual(sent[1]['content'], '4')
        self.assertEqual([m['role'] for m in sent[1:-1]], ['user', 'assistant'] * 6)

    def test_clear_removes_prior_messages(self):
        self.bot.ask("old")
        self.bot.clear()
        self.bot.ask("new")
        self.assertEqual(len(self.client.complete.call_args.args[0]), 2)

    def test_failure_does_not_enter_history(self):
        self.bot.ask("first")
        self.client.complete.side_effect = ChatError("failed")
        with self.assertRaises(ChatError):
            self.bot.ask("failed question")
        self.client.complete.side_effect = None
        self.bot.ask("retry")
        self.assertNotIn('failed question', [m['content'] for m in self.client.complete.call_args.args[0]])

    def test_bad_questions_do_not_call_api(self):
        for question in ('', '  ', None, 'x' * 4001):
            with self.assertRaises(ValueError):
                self.bot.ask(question)
        self.client.complete.assert_not_called()

    def test_empty_answer_does_not_enter_history(self):
        self.client.complete.return_value = ''
        with self.assertRaises(ChatError):
            self.bot.ask('hello')
        self.assertEqual(self.bot._history, [])


class ProviderTests(unittest.TestCase):
    def test_missing_key(self):
        with self.assertRaises(ValueError):
            MistralClient(' ')

    def response(self, reason='stop', content='Example answer'):
        return json.dumps({'choices': [{'message': {'content': content}, 'finish_reason': reason}]}).encode()

    @patch('health_bot.http.client.HTTPSConnection')
    def test_request_and_response(self, factory):
        conn = factory.return_value
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read.return_value = self.response()
        answer = MistralClient('test-only-key').complete([{'role': 'user', 'content': 'test'}])
        self.assertEqual(answer, 'Example answer')
        self.assertEqual(factory.call_args.args[0], 'api.mistral.ai')
        payload = json.loads(conn.request.call_args.kwargs['body'])
        self.assertEqual(payload['max_tokens'], 600)
        self.assertEqual(payload['messages'][0]['content'], 'test')
        conn.close.assert_called_once()

    @patch('health_bot.http.client.HTTPSConnection')
    def test_http_error_redacts_provider_body(self, factory):
        conn = factory.return_value
        conn.getresponse.return_value.status = 401
        conn.getresponse.return_value.read.return_value = b'secret provider body'
        with self.assertRaises(ChatError) as error:
            MistralClient('test-only-key').complete([])
        self.assertNotIn('test-only-key', str(error.exception))
        self.assertNotIn('secret provider body', str(error.exception))
        conn.close.assert_called_once()

    @patch('health_bot.http.client.HTTPSConnection')
    def test_invalid_json_is_safe_error(self, factory):
        conn = factory.return_value
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read.return_value = b'not json'
        with self.assertRaises(ChatError):
            MistralClient('test-only-key').complete([])

    @patch('health_bot.http.client.HTTPSConnection')
    def test_truncation_is_reported(self, factory):
        conn = factory.return_value
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read.return_value = self.response(reason='length')
        self.assertIn('may be incomplete', MistralClient('test-only-key').complete([]))

    @patch('health_bot.http.client.HTTPSConnection')
    def test_timeout_is_safe_error(self, factory):
        factory.return_value.request.side_effect = TimeoutError('sensitive transport detail')
        with self.assertRaises(ChatError) as error:
            MistralClient('test-only-key').complete([])
        self.assertNotIn('sensitive transport detail', str(error.exception))


if __name__ == '__main__':
    unittest.main()
