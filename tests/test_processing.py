import unittest

from app.processing import classify_scene, create_scene_plan, validate_request


class ProcessingTests(unittest.TestCase):
    def test_validate_supported_request(self):
        result = validate_request("Dois personagens andando", "5", "16:9")
        self.assertTrue(result["ok"])

    def test_empty_description_is_rejected(self):
        result = validate_request("   ", "5", "16:9")
        self.assertFalse(result["ok"])

    def test_supported_scene_classification(self):
        self.assertEqual(classify_scene("Dois bonequinhos jogando futebol"), "soccer")
        self.assertEqual(classify_scene("Um personagem caminhando"), "walking")
        self.assertEqual(classify_scene("Duplas conversando no parque"), "talking")

    def test_unknown_scene_is_rejected(self):
        with self.assertRaises(ValueError):
            create_scene_plan("Um astronauta no planeta Marte", 5, "16:9")

    def test_invalid_duration_and_format_are_rejected(self):
        self.assertFalse(validate_request("Andando", "20", "16:9")["ok"])
        self.assertFalse(validate_request("Andando", "5", "1:1")["ok"])


if __name__ == "__main__":
    unittest.main()
