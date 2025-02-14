# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
import logging
import sys

from telemetry.testing import run_tests


def RunChromeOSTests(browser_type, tests_to_run):
  """ Run ChromeOS tests.
  Args:
    |browser_type|: string specifies which browser type to use.
    |tests_to_run|: a list of tuples (top_level_dir, unit_tests), whereas
      |top_level_dir| specifies the top level directory for running tests, and
      |unit_tests| is a list of string test names to run.
  """
  std_out, std_err = (
      _LoggingOutputStream(sys.stdout), _LoggingOutputStream(sys.stderr))
  error_string = ''

  for (top_level_dir, unit_tests) in tests_to_run:
    logging.info('Running unit tests in %s with browser_type "%s".' %
                 (top_level_dir, browser_type))

    ret = _RunOneSetOfTests(
        browser_type, top_level_dir, unit_tests, std_out, std_err)
    if ret:
      error_string += 'The unit tests of %s failed.\n' % top_level_dir
  return error_string


def _RunOneSetOfTests(browser_type, top_level_dir, tests, std_out, std_err):
  args = ['--browser', browser_type,
          '--top-level-dir', top_level_dir,
          '--jobs', '1',
          '--disable-logging-config'] + tests
  return run_tests.RunTestsCommand.main(args, std_out=std_out, std_err=std_err)


class _LoggingOutputStream(object):

  def __init__(self, stream):
    self._buffer = []
    self._stream = stream

  def write(self, s):
    """Buffer a string write. Log it when we encounter a newline."""
    if '\n' in s:
      segments = s.split('\n')
      segments[0] = ''.join(self._buffer + [segments[0]])
      log_level = logging.getLogger().getEffectiveLevel()
      try:  # TODO(dtu): We need this because of crbug.com/394571
        logging.getLogger().setLevel(logging.INFO)
        for line in segments[:-1]:
          logging.info(line)
      finally:
        logging.getLogger().setLevel(log_level)
      self._buffer = [segments[-1]]
    else:
      self._buffer.append(s)

  def flush(self):
    pass

  def fileno(self):
    return self._stream.fileno()

  @property
  def mode(self):
    """autotest monkey patches sys.stdout and sys.stderr with
    LoggingFile objects. These objects underlying stream are opened
    in read only mode. When Typ's host module attemps to open a duplicate
    file descriptor for the LoggingFile stream it must set the file
    mode to 'r'.
    """
    return 'r'

  def isatty(self):
    return self._stream.isatty()

