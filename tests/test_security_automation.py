import importlib.util
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('automation',Path(__file__).parents[1]/'scripts/security_automation.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class AutomationTests(unittest.TestCase):
    def test_failed_package_query_is_not_reported_as_success(self):
        with patch.object(module.subprocess,'run',side_effect=subprocess.CalledProcessError(1,['pip'])):
            self.assertEqual(module.check_for_updates(),1)

    def test_help_does_not_contact_package_index(self):
        with patch.object(module.subprocess,'run') as run:
            self.assertEqual(module.main([]),0);run.assert_not_called()

    def test_extension_points_are_explicitly_unimplemented(self):
        for check in [module.verify_ssl_certificates,module.monitor_system_logs]:
            with self.assertRaises(NotImplementedError):check()

if __name__=='__main__':unittest.main()
