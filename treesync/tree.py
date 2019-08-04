
import asyncio
import locale
import sys


class Tree:
    """
    Configuration for a single tree
    """
    def __init__(self, config, name, src, dest, flags=None, error_callback=None, message_callback=None):
        self.config = config
        self.name = name
        self.src = src.rstrip('/')
        self.dest = dest.rstrip('/')
        self.flags = flags if flags else []

        self.message_callback = message_callback if message_callback is not None else self.__stdout__
        self.error_callback = error_callback if error_callback is not None else self.__stderr__

    def __eq__(self, value):
        return self.name == value

    def _ne__(self, value):
        return self.name != value

    def __lt__(self, value):
        return self.name < value

    def __le__(self, value):
        return self.name <= value

    def __gt__(self, value):
        return self.name > value

    def __ge__(self, value):
        return self.name >= value

    def __stdout__(self, message):
        if not self.config.quiet:
            return sys.stdout.write('{}\n'.format(message))

    def __stderr__(self, message):
        if not self.config.quiet:
            return sys.stderr.write('{}\n'.format(message))

    def __run__(self, args):
        """
        Run the command, printing output if requested
        """

        if self.config.debug:
            self.__stdout__(' '.join(args))

        async def run_process():
            process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            async for line in process.stdout:
                if line == '':
                    break
                self.message_callback(line.decode(locale.getpreferredencoding(False)).rstrip())

            async for line in process.stderr:
                if line == '':
                    break
                self.error_callback(line.decode(locale.getpreferredencoding(False)).rstrip())

            return await process.wait()

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(run_process())

    def pull(self, dry_run=False):
        """
        Pull tree to src from dest
        """
        flags = self.flags
        if dry_run:
            flags.append('--dry-run')
        cmd = ['rsync'] + flags + ['{}/'.format(self.dest), '{}/'.format(self.src)]
        self.__run__(cmd)

    def push(self, dry_run=False):
        """
        Push tree to dest from src
        """
        flags = self.flags
        if dry_run:
            flags.append('--dry-run')
        cmd = ['rsync'] + flags + ['{}/'.format(self.src), '{}/'.format(self.dest)]
        self.__run__(cmd)
