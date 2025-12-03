import time


class LogManager:
    def __init__(self, log_file='Log.txt'):
        self.log_file = log_file
        self.event_counter = 0  
    
    def get_timestamp(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    def generate_event_id(self):
        self.event_counter += 1
        return f"E{self.event_counter:04d}"  
    
    def write_to_file(self, log_message):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def log(self, level, source, message, user=None, additional_info=None):
        timestamp = self.get_timestamp()
        event_id = self.generate_event_id()
        
        log_entry = f"{timestamp} | {level.upper()} | [{source}] ID:{event_id} - {message}"
        
        if user:
            log_entry += f" | User: {user}"
        
        if additional_info:
            log_entry += f" | Info: {additional_info}"
        
        self.write_to_file(log_entry)
    
    def info(self, source, message, user=None, additional_info=None):
        self.log('INFO', source, message, user, additional_info)
    
    def debug(self, source, message, user=None, additional_info=None):
        self.log('DEBUG', source, message, user, additional_info)
    
    def warning(self, source, message, user=None, additional_info=None):
        self.log('WARN', source, message, user, additional_info)
    
    def error(self, source, message, user=None, additional_info=None):
        self.log('ERROR', source, message, user, additional_info)
    
    def fatal(self, source, message, user=None, additional_info=None):
        self.log('FATAL', source, message, user, additional_info)


if __name__ == '__main__':
    log_manager = LogManager('Log.txt')
    log_manager.info('File', 'File launched')
    log_manager.debug('Database', 'Database connected', user='admin', additional_info='SQL')
    log_manager.warning('API', 'Slow answer from server', user='user123', additional_info='5.2 sec')
    log_manager.error('FileSystem', 'File not found', additional_info='path: /data/homework.py')
    log_manager.fatal('System', 'OEM', user='system', additional_info='Out of video memory trying to allocate a rendering resource')
    print("Логи записаны в файл Log.txt")
