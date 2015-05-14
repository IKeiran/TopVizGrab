import gearman

gm_worker = gearman.GearmanWorker(['app.gearmanhq.com:4735'])

#  define method to handled 'reverse' work
def task_listener_reverse(gearman_worker, gearman_job):
  print 'reporting status'
  return reversed(gearman_job.data)

gm_worker.set_client_id('your_worker_client_id_name')
gm_worker.register_task('reverse', task_listener_reverse)

gm_worker.work()