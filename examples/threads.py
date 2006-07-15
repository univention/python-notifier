import notifier
import notifier.threads as threads

import time

def my_thread( words ):
    i = 50
    while i:
	print i, words
	time.sleep( 0.1 )
	i -= 1
    return words.reverse()

def done_with_it( thread, result ):
    print "Thread '%s' is finished" % thread.name()
    print "Result:", result

def doing_something_else():
    print 'doing something else'
    return True

if __name__ == '__main__':
    notifier.init( notifier.GENERIC )

#     notifier.dispatcher_add( threads.results )
    task = threads.Thread( 'test',
			   notifier.Callback( my_thread, [ 'hello', 'world' ] ),
			   done_with_it )
    task.run()
    notifier.timer_add( 1000, doing_something_else )
    notifier.loop()
