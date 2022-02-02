import paramiko


class FileExplorer:
    """
    Python class that handles listing, renaming, viewing,
    deleting, adding of files in user's remote directory through ssh\sftp
    """

    def __init__(self, userid, passwd, host_id):
        """Create and return a FileExplorer object"""
        try:
            self.ssh_server = paramiko.SSHClient()
            self.ssh_server.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            try:
                self.ssh_server.connect(host_id, username=userid,
                                        password=passwd)
            except Exception as e:
                print 'error: ', e.message
        except Exception as e:
            raise e

    def isLive(self):
        """Checks if ssh is live"""
        return self.ssh_server.get_transport().is_active()

    def close(self):
        """Close the connection if it's active"""
        self.ssh_server.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def listFiles(self, root='.'):
        """Recursively list all files and return their tree representation
            which is a hierarchial element
        """
        # Prepare the python module for server upload
        # The module should be hidden
        moveFile = '.fileLister.py'
        # First copy the file from root to user directory, in case user has
        # deleted it accidentally, file is already present at root and that
        # version cannot be deleted
        cmd = "cp /%s ." % (moveFile)
        stdin, stdout, stderr = self.ssh_server.exec_command(cmd, bufsize=-1)

        stdin, stdout, stderr = self.ssh_server.exec_command(
            'python ' + moveFile, bufsize=-1)

        # if stderr is empty, then success
        error, output = '', ''
        for line in stderr.readlines():
            error += line
        if error != '':
            raise Exception(error)
        for line in stdout.readlines():
            output += line
        return output

    def executeJSONList(self, username):
        """Recursively list all files and return their JSON
            for use in the file explorer window in home
        """
        # The jsonPyFile (stored at root) will be executed and the result
        # captured
        jsonPyFile = '.dirExplorer.py'
        # self.sftp_server.upload('editor/scripts/%s' %
        #                         (moveFile), "./.%s" % (moveFile))
        stdin, stdout, stderr = self.ssh_server.exec_command(
            'python ' + '/%s /home/%s' % (jsonPyFile, username), bufsize=-1)

        # if stderr is empty, then success
        error, output = '', ''
        for line in stderr.readlines():
            error += line
        if error != '':
            raise Exception(error)
        for line in stdout.readlines():
            output += line
        # print 'output: ', output
        return output

    def viewRemoteFile(self, remote_path):
        """View file contents of the remote_path at the server"""
        cmd = "cat \"%s\"" % (remote_path)
        print 'cmd: ', cmd
        stdin, stdout, stderr = self.ssh_server.exec_command(
            cmd, timeout=2)

        # if stderr is empty, then success
        error, output = '', ''
        for line in stderr.readlines():
            error += line
        if error != '':
            print error
            raise Exception(error)
        for line in stdout.readlines():
            output += line
        return output

    def deleteRemoteFile(self, remote_path):
        """View file contents of the remote_path at the server"""
        cmd = "rm -r \"%s\"" % (remote_path)
        print 'cmd: ', cmd
        stdin, stdout, stderr = self.ssh_server.exec_command(
            cmd, timeout=2)

        # if stderr is empty, then success
        error = ''
        for line in stderr.readlines():
            error += line
        if error != '':
            print error
            raise Exception(error)

    def saveUserConfig(self, data):
        """Saves user data to a config file"""
        configFile = '.config'
        pictureFile = '.picture'
        text = ''
        pictureText = data['picture']

        for k, v in data.iteritems():
            if k != 'picture':
                text += '%s: %s\n' % (k, v)
        print 'Im saving text: ', text
        cmd = "cat > %s << \'endmsg\'\n%s\nendmsg" % (
            configFile, text)
        stdin, stdout, stderr = self.ssh_server.exec_command(
            cmd, timeout=2)
        storeFileCmd = "cat > %s << \'endmsg\'\n%s\nendmsg" % (
            pictureFile, pictureText)
        stdin, stdout, stderr = self.ssh_server.exec_command(
            storeFileCmd, timeout=2)
        error = ''
        for line in stderr.readlines():
            error += line
        if error != '':
            print error
            raise Exception(error)

    def loadUserConfig(self):
        """Loads user data from a config file"""
        configFile = '.config'
        pictureFile = '.picture'
        userConfig = self.viewRemoteFile(configFile)
        userConfigData = {}
        pictureConfig = str(self.viewRemoteFile(pictureFile))
        userConfigData['picture'] = str(pictureConfig)

        for i in userConfig.strip().split("\n"):
            k, v = i.split(':')
            userConfigData[k] = v
        return userConfigData

    def saveFileToRemote(self, remote_path, file_name, content):
        """View file contents of the remote_path at the server"""
        print remote_path, file_name, content
        print '***********'
        cmd = "cat > \"%s/%s\" << \'endmsg\'\n%s\nendmsg" % (
            remote_path, file_name, content)
        stdin, stdout, stderr = self.ssh_server.exec_command(
            cmd, timeout=2)
        print 'save: ', cmd
        # if stderr is empty, then success
        error = ''
        for line in stderr.readlines():
            error += line
        if error != '':
            print error
            raise Exception(error)

    def makeRemoteDirectory(self, remote_path, is_file):
        """View file contents of the remote_path at the server"""
        outputResponse = "File created successfully"
        # Also check whether .Testcases folder exists or not,
        # if not create it. Hint: use mkdir -p command
        testcaseFolder = 'Testcases'
        cmd = 'mkdir -p %s' % (testcaseFolder)
        stdin, stdout, stderr = self.ssh_server.exec_command(
            cmd, timeout=2)

        cmd = 'touch \"%s\"' % (remote_path)
        if is_file == "False":
            outputResponse = "Folder created successfully"
            cmd = "mkdir \"%s\"" % (remote_path)
        print 'cmd: ', cmd
        stdin, stdout, stderr = self.ssh_server.exec_command(
            cmd, timeout=2)

        # if stderr is empty, then success
        error = ''
        for line in stderr.readlines():
            error += line
        if error != '':
            print error
            raise Exception(error)
        return outputResponse

    def renameRemoteFile(self, remote_path, new_path):
        """View file contents of the remote_path at the server"""
        cmd = "mv \"%s\" \"%s\"" % (remote_path, new_path)
        print 'cmd: ', cmd
        stdin, stdout, stderr = self.ssh_server.exec_command(
            cmd, timeout=2)

        # if stderr is empty, then success
        error = ''
        for line in stderr.readlines():
            error += line
        if error != '':
            print error
            raise Exception(error)

    def execute_CompileCode(self, code, lang, uid, inp, name, parDir, curDir):
        """Recursively list all files and return their JSON
            for use in the file explorer window in home
        """
        saveName = '%s.%s' % (name, lang) if lang != "" else name
        try:
            # Save current file to remote
            self.saveFileToRemote(parDir, saveName, code)
            # Now begin compiling and running the code
            # The jsonPyFile will be executed and the result captured
            executePyFile = '.codeExecuter.py'
            cmd = "python  /%s  \"%s\"  \"%s\" \"%s\"\
            \"%s\" \"%s\"" % (
                executePyFile, curDir, lang, uid, inp, name)
            stdin, stdout, stderr = self.ssh_server.exec_command(
                cmd, timeout=3)

            # if stderr is empty, then success
            error, output = '', ''
            for line in stderr.readlines():
                error += line
            if error != '':
                raise Exception(error)
            for line in stdout.readlines():
                output += line
            return output
        except Exception as e:
            return e
