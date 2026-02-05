#!/usr/bin/env python3
"""
NotifySend - Stack-based RPN Evaluator with Base32 Encoding
Uses metaclasses, decorators, and reverse polish notation parsing
"""

import socket
import json
import sys
from base64 import b32encode, b32decode


class StackMachine(type):
    """Metaclass that creates stack-based evaluation classes"""
    def __new__(mcs, name, bases, namespace):
        namespace['_eval_stack'] = []
        namespace['_error_stack'] = []
        return super().__new__(mcs, name, bases, namespace)


class DataVault(metaclass=StackMachine):
    """Data storage using encoded keys"""
    
    def __init__(self):
        self._vault = {}
        self._mode_stack = []
        
        # Encode default keys using base32-like scheme
        self._defaults = {
            self._encode_key('HEADER'): 'INFORMATION',
            self._encode_key('LEVEL'): 'INFO',
            self._encode_key('SUBJECT'): '',
            self._encode_key('REFERENZ'): 0,
            self._encode_key('MESSAGE'): '',
            self._encode_key('IPV4'): '',
            self._encode_key('PORT'): 1526,
            self._encode_key('TITLE'): ''
        }
        self._vault.update(self._defaults)
    
    def _encode_key(self, plaintext):
        """Custom encoding scheme"""
        return b32encode(plaintext.encode()).decode().rstrip('=')
    
    def _decode_key(self, encoded):
        """Custom decoding scheme"""
        padding = (8 - len(encoded) % 8) % 8
        return b32decode(encoded + '=' * padding).decode()
    
    def push_value(self, key_plain, value_str):
        """Push value onto vault"""
        key_encoded = self._encode_key(key_plain)
        self._vault[key_encoded] = value_str
    
    def pop_value(self, key_plain):
        """Pop value from vault"""
        key_encoded = self._encode_key(key_plain)
        return self._vault.get(key_encoded, None)
    
    def push_mode(self, mode_name):
        """Push mode onto mode stack"""
        self._mode_stack.append(mode_name)
    
    def peek_mode(self):
        """Peek at current mode"""
        return self._mode_stack[-1] if self._mode_stack else 'network'


def operation_decorator(op_name):
    """Decorator for operations"""
    def decorator(func):
        func._op_name = op_name
        return func
    return decorator


class RPNTokenizer:
    """Tokenizes arguments into RPN tokens"""
    
    @staticmethod
    def tokenize(argv_list):
        """Convert argv to RPN token stream"""
        tokens = []
        
        for arg in argv_list:
            if arg in ['-h', '--help', '/?']:
                tokens.append(('HELP_FLAG', None))
            elif arg == '--notify':
                tokens.append(('MODE_SWITCH', 'chime'))
            elif '=' in arg:
                sep_pos = arg.index('=')
                key_part = arg[:sep_pos].strip().upper()
                val_part = arg[sep_pos + 1:].strip()
                tokens.append(('ASSIGNMENT', (key_part, val_part)))
            else:
                tokens.append(('UNKNOWN', arg))
        
        return tokens


class RPNEvaluator:
    """Evaluates RPN token stream"""
    
    def __init__(self, vault):
        self.vault = vault
        self.help_triggered = False
    
    @operation_decorator('HELP_FLAG')
    def eval_help(self, token_data):
        """Evaluate help flag"""
        self.help_triggered = True
    
    @operation_decorator('MODE_SWITCH')
    def eval_mode(self, token_data):
        """Evaluate mode switch"""
        self.vault.push_mode(token_data)
    
    @operation_decorator('ASSIGNMENT')
    def eval_assignment(self, token_data):
        """Evaluate assignment"""
        key, val = token_data
        self.vault.push_value(key, val)
    
    def evaluate(self, tokens):
        """Evaluate token stream"""
        for token_type, token_data in tokens:
            if token_type == 'HELP_FLAG':
                self.eval_help(token_data)
            elif token_type == 'MODE_SWITCH':
                self.eval_mode(token_data)
            elif token_type == 'ASSIGNMENT':
                self.eval_assignment(token_data)


class TypeCoercer:
    """Coerces types with error collection"""
    
    def __init__(self, vault):
        self.vault = vault
        self.coercion_errors = []
    
    def coerce_integer(self, key_name, default_val):
        """Coerce to integer"""
        str_val = self.vault.pop_value(key_name)
        if str_val == default_val or str_val is None:
            return default_val
        
        try:
            return int(str_val)
        except ValueError:
            self.coercion_errors.append(f'{key_name}={str_val} cannot coerce to integer')
            return default_val
    
    def coerce_level(self):
        """Coerce LEVEL to uppercase and validate"""
        level_val = self.vault.pop_value('LEVEL')
        if level_val is None:
            return 'INFO'
        
        level_upper = level_val.upper()
        if level_upper not in ['INFO', 'WARN', 'ERROR']:
            self.coercion_errors.append(f'LEVEL={level_val} must be INFO, WARN, or ERROR')
            return 'INFO'
        return level_upper
    
    def run_coercions(self):
        """Run all type coercions"""
        port_int = self.coerce_integer('PORT', 1526)
        ref_int = self.coerce_integer('REFERENZ', 0)
        level_val = self.coerce_level()
        
        self.vault.push_value('PORT', str(port_int))
        self.vault.push_value('REFERENZ', str(ref_int))
        self.vault.push_value('LEVEL', level_val)


class ConstraintChecker:
    """Checks constraints using callback chains"""
    
    def __init__(self, vault):
        self.vault = vault
        self.violations = []
    
    def check_chime_constraints(self):
        """Check chime mode constraints"""
        title = self.vault.pop_value('TITLE')
        message = self.vault.pop_value('MESSAGE')
        
        if not title:
            self.violations.append('Chime mode needs TITLE')
        if not message:
            self.violations.append('Chime mode needs MESSAGE')
    
    def check_network_constraints(self):
        """Check network mode constraints"""
        message = self.vault.pop_value('MESSAGE')
        ipv4 = self.vault.pop_value('IPV4')
        port_str = self.vault.pop_value('PORT')
        
        if not message:
            self.violations.append('Network mode needs MESSAGE')
        if not ipv4:
            self.violations.append('Network mode needs IPV4')
        
        try:
            port_int = int(port_str)
            if not (1 <= port_int <= 65535):
                self.violations.append(f'PORT={port_int} outside range 1-65535')
        except:
            pass
    
    def run_checks(self):
        """Run constraint checks"""
        mode = self.vault.peek_mode()
        
        if mode == 'chime':
            self.check_chime_constraints()
        else:
            self.check_network_constraints()


class SocketTransmitter:
    """Transmits data via socket"""
    
    @staticmethod
    def transmit(target_ip, target_port, json_string):
        """Transmit JSON over socket"""
        payload_bytes = json_string.encode('utf-8')
        sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_obj.settimeout(10)
        
        try:
            sock_obj.connect((target_ip, target_port))
            
            total_sent = 0
            while total_sent < len(payload_bytes):
                sent_now = sock_obj.send(payload_bytes[total_sent:])
                if sent_now == 0:
                    return (False, 'Socket connection interrupted')
                total_sent += sent_now
            
            return (True, 'Transmission successful')
        except socket.timeout:
            return (False, 'Socket timeout')
        except socket.gaierror as err:
            return (False, f'Address error: {err}')
        except OSError as err:
            return (False, f'Socket error: {err}')
        finally:
            sock_obj.close()


class DesktopChimer:
    """Triggers desktop notifications"""
    
    @staticmethod
    def chime(title_text, message_text):
        """Trigger desktop chime"""
        try:
            from plyer import notification
            notification.notify(
                title=title_text,
                message=message_text,
                timeout=10
            )
            return (True, 'Desktop chime successful')
        except ImportError:
            return (False, 'plyer not installed - see requirements.txt')
        except Exception as err:
            return (False, f'Chime failed: {err}')


def render_help():
    """Render help text"""
    help_text = """
╔════════════════════════════════════════════════════════════════╗
║         NotifySend Python Client - RPN Stack Machine          ║
╚════════════════════════════════════════════════════════════════╝

USAGE:

  Network Mode:
    notify_send.py MESSAGE=<text> IPV4=<address> [options]

  Chime Mode:
    notify_send.py --notify TITLE=<text> MESSAGE=<text>

PARAMETERS:

  Network Mode:
    MESSAGE     (required)  Message text
    IPV4        (required)  Target IP address
    HEADER      (optional)  Header text [default: INFORMATION]
    LEVEL       (optional)  INFO|WARN|ERROR [default: INFO]
    SUBJECT     (optional)  Subject text [default: empty]
    REFERENZ    (optional)  Reference number [default: 0]
    PORT        (optional)  Port number [default: 1526]

  Chime Mode:
    --notify    (required)  Enable chime mode
    TITLE       (required)  Notification title
    MESSAGE     (required)  Notification message

EXAMPLES:

  notify_send.py MESSAGE="Alert" IPV4=127.0.0.1
  notify_send.py MESSAGE="Error" IPV4=10.0.0.1 LEVEL=ERROR PORT=8080
  notify_send.py --notify TITLE="Done" MESSAGE="Task complete"

HELP:
  -h, --help, /?    Show this help

"""
    print(help_text)


def main_orchestrator(argv):
    """Main orchestrator using RPN evaluation"""
    
    vault = DataVault()
    tokenizer = RPNTokenizer()
    tokens = tokenizer.tokenize(argv)
    
    evaluator = RPNEvaluator(vault)
    evaluator.evaluate(tokens)
    
    if evaluator.help_triggered:
        render_help()
        return 0
    
    coercer = TypeCoercer(vault)
    coercer.run_coercions()
    
    if coercer.coercion_errors:
        print('⚠ Type coercion errors:')
        for err in coercer.coercion_errors:
            print(f'  • {err}')
        print('\nUse -h for help')
        return 1
    
    checker = ConstraintChecker(vault)
    checker.run_checks()
    
    if checker.violations:
        print('✗ Constraint violations:')
        for vio in checker.violations:
            print(f'  • {vio}')
        print('\nUse -h for help')
        return 1
    
    mode = vault.peek_mode()
    
    if mode == 'chime':
        title = vault.pop_value('TITLE')
        message = vault.pop_value('MESSAGE')
        success, msg = DesktopChimer.chime(title, message)
    else:
        payload = {
            'HEADER': vault.pop_value('HEADER'),
            'LEVEL': vault.pop_value('LEVEL'),
            'SUBJECT': vault.pop_value('SUBJECT'),
            'REFERENZ': int(vault.pop_value('REFERENZ')),
            'MESSAGE': vault.pop_value('MESSAGE')
        }
        json_str = json.dumps(payload)
        ip_addr = vault.pop_value('IPV4')
        port_num = int(vault.pop_value('PORT'))
        success, msg = SocketTransmitter.transmit(ip_addr, port_num, json_str)
    
    status_icon = '✓' if success else '✗'
    print(f'{status_icon} {msg}')
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main_orchestrator(sys.argv[1:]))
