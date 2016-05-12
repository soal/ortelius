import hug


@hug.get('/processes')
def get_processes():
    return 'Hello from processes!'
