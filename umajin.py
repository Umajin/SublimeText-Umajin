import os
import sublime
import sublime_plugin


#from lib.command_thread import CommandThread

# Fun discovery: Sublime on windows still requires posix path separators.

PLUGIN_DIRECTORY = os.getcwd().replace(os.path.normpath(os.path.join(os.getcwd(), '..', '..')) + os.path.sep, '').replace(os.path.sep, '/')
PLUGIN_PATH = os.getcwd().replace(os.path.join(os.getcwd(), '..', '..') + os.path.sep, '').replace(os.path.sep, '/')

# def open_url(url):
#   sublime.active_window().run_command('open_url', {"url": url})

# def view_contents(view):
#   region = sublime.Region(0, view.size())
#   return view.substr(region)

# def plugin_file(name):
#   return os.path.join(PLUGIN_DIRECTORY, name)

class UmajinCommand(sublime_plugin.TextCommand):
  def run_command(self, command, callback=None, show_status=True, filter_empty_args=True, **kwargs):
    if filter_empty_args:
      command = [arg for arg in command if arg]
    if 'working_dir' not in kwargs:
      kwargs['working_dir'] = self.get_working_dir()
    s = sublime.load_settings("Umajin.sublime-settings")
    if s.get('save_first') and self.active_view() and self.active_view().is_dirty():
      self.active_view().run_command('save')
    if command[0] == 'umajin' and s.get('umajin_command'):
      command[0] = s.get('umajin_command')
    if command[0] == 'npm' and s.get('npm_command'):
      command[0] = s.get('npm_command')
    if not callback:
      callback = self.generic_done

    thread = CommandThread(command, callback, **kwargs)
    thread.start()

    if show_status:
      message = kwargs.get('status_message', False) or ' '.join(command)
      sublime.status_message(message)

  def generic_done(self, result):
    if not result.strip():
      return
    self.panel(result)

  def _output_to_view(self, output_file, output, clear=False, syntax="Packages/Umajin/Umajin.tmLanguage"):
    output_file.set_syntax_file(syntax)
    edit = output_file.begin_edit()
    if clear:
      region = sublime.Region(0, self.output_view.size())
      output_file.erase(edit, region)
    output_file.insert(edit, 0, output)
    output_file.end_edit(edit)

  def scratch(self, output, title=False, **kwargs):
    scratch_file = self.get_window().new_file()
    if title:
      scratch_file.set_name(title)
    scratch_file.set_scratch(True)
    self._output_to_view(scratch_file, output, **kwargs)
    scratch_file.set_read_only(True)
    return scratch_file

  def panel(self, output, **kwargs):
    if not hasattr(self, 'output_view'):
      self.output_view = self.get_window().get_output_panel("git")
    self.output_view.set_read_only(False)
    self._output_to_view(self.output_view, output, clear=True, **kwargs)
    self.output_view.set_read_only(True)
    self.get_window().run_command("show_panel", {"panel": "output.git"})

  def quick_panel(self, *args, **kwargs):
    self.get_window().show_quick_panel(*args, **kwargs)

# A base for all git commands that work with the file in the active view
class UmajinTextCommand(UmajinCommand, sublime_plugin.TextCommand):
  def active_view(self):
    return self.view

  def is_enabled(self):
    # First, is this actually a file on the file system?
    if self.view.file_name() and len(self.view.file_name()) > 0:
      return os.path.realpath(self.get_working_dir())

  def get_file_name(self):
    return os.path.basename(self.view.file_name())

  def get_working_dir(self):
    return os.path.dirname(self.view.file_name())

  def get_window(self):
    # Fun discovery: if you switch tabs while a command is working,
    # self.view.window() is None. (Admittedly this is a consequence
    # of my deciding to do async command processing... but, hey,
    # got to live with that now.)
    # I did try tracking the window used at the start of the command
    # and using it instead of view.window() later, but that results
    # panels on a non-visible window, which is especially useless in
    # the case of the quick panel.
    # So, this is not necessarily ideal, but it does work.
    return self.view.window() or sublime.active_window()
    
  def get_root_folder(self):
    root_folder = self.get_window().folders()[0]
    #TODO: If no umajin.exe in root_folder, then try finding it starting in current files dir, then back through parent dirs.
    
    # custom_exe_path = view.settings().get('umajin_exe_path')
    # custom_exe_path = sublime.load_settings("Umajin.sublime-settings").get('umajin_exe_path')
    # if (not custom_exe_path):
    #   root_folder = custom_exe_path
    return root_folder


### Run Commands ###

# Command to Run Umajin
class UmajinRunCommand(UmajinTextCommand):
  def run(self, edit):
    root_folder = self.get_root_folder()
    umajin_exe = root_folder + '\\umajin.exe'
    start_file = root_folder + '\\start.u'
    command_string = umajin_exe+" --all-warnings --output=stdout --log-format=p:ti:t:d "+start_file+" | C:\\Umajin3_debug_GUI\\umajin3_debug_gui.exe -r "+root_folder
    command = ["cmd", "/c", command_string]
    self.get_window().run_command("exec", {"cmd": command})
 
# Command to Run Umajin file
class UmajinFileRunCommand(UmajinTextCommand):
  def run(self, edit):
    root_folder = self.get_root_folder()
    umajin_exe = root_folder + '\\umajin.exe';
    start_file = self.view.file_name() # root_folder + '\\start.u'
    command_string = umajin_exe+" --all-warnings --output=stdout --log-format=p:ti:t:d "+start_file+" | C:\\Umajin3_debug_GUI\\umajin3_debug_gui.exe -r "+root_folder
    command = ["cmd", "/c", command_string]
    self.get_window().run_command("exec", {"cmd": command})

# Command to Run Umajin in Metro
class UmajinMetroRunCommand(UmajinTextCommand):
  def run(self, edit):
    root_folder = self.get_root_folder()
    command = ["cmd", "/c", "C:\\Users\\adamh\\Documents\\Dev\\Projects\\UnlimitedRealities\\UmajinAppBuilder\\umajin_app_builder\\app_builder.url"]
    self.get_window().run_command("exec", {"cmd": command})
    
# Command to Run Umajin in Metro
class UmajinDebugGuiRunCommand(UmajinTextCommand):
  def run(self, edit):
    root_folder = self.get_root_folder()
    command_string = "umajin3_debug_gui.exe -x -e C:\\Users\\adamh\\AppData\\Local\\Packages\\umajin_kfxajk8fbbyc2\\LocalState\\messages.txt -s 127.0.0.1 -r "+root_folder
    command = ["cmd", "/c", command_string]
    self.get_window().run_command("exec", {"cmd": command})

class UmajinTestRunCommand(UmajinTextCommand):
  def run(self, edit):
    root_folder = self.get_root_folder()
    umajin_exe = root_folder + '\\umajin.exe'
    start_file = root_folder + '\\run_tests.u'
    # command_string = umajin_exe+" --all-warnings --output=stdout --log-format=p:ti:t:d "+start_file+" -minimal | C:\\Umajin3_debug_GUI\\umajin3_debug_gui.exe -r "+root_folder
    command_string = umajin_exe+" --all-warnings --output=stdout --log-format=p:ti:t:d "+start_file+" | C:\\Umajin3_debug_GUI\\umajin3_debug_gui.exe -r "+root_folder
    command = ["cmd", "/c", command_string]
    self.get_window().run_command("exec", {"cmd": command})
  
class UmajinRegressionTestRunCommand(UmajinTextCommand):
  def run(self, edit):
    # DEL test_runner.txt /Q
    # UMAJIN.EXE --all-warnings --output=stdout --log-format=p:ti:t:d regression_runner.u -minimal | "C:\Umajin\Umajin3_debug_GUI\umajin3_debug_gui.exe" --stdout >test_runner.txt
    root_folder = self.get_root_folder()
    umajin_exe = root_folder + '\\umajin.exe'
    start_file = root_folder + '\\regression_runner.u'
    # command_string = umajin_exe+" --all-warnings --output=stdout --log-format=p:ti:t:d "+start_file+" -minimal | C:\\Umajin\\Umajin3_debug_GUI\\umajin3_debug_gui.exe -r "+root_folder
    command_string = umajin_exe+" --all-warnings --output=stdout --log-format=p:ti:t:d "+start_file+" -minimal | C:\\Umajin3_debug_GUI\\umajin3_debug_gui.exe -r "+root_folder+" --stdout >test_runner.txt"
    command = ["cmd", "/c", command_string]
    self.get_window().run_command("exec", {"cmd": command})
