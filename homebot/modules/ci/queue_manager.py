from homebot.core.error_handler import format_exception
from homebot.core.logging import LOGE, LOGI
from queue import Queue
import threading

class QueueManager:
	def __init__(self):
		self.queue = Queue()
		self.current_workflow = None
		self.ci_thread = threading.Thread(target=self.run, name="CI workflows")
		self.ci_thread.start()

	def run(self):
		while True:
			try:
				self.current_workflow = self.queue.get()
				workflow_name = self.current_workflow.project_name
				LOGI(f"CI workflow started, project: {workflow_name}")
				try:
					self.current_workflow.run()
				except Exception as e:
					message = "Unhandled exception from CI workflow:"
					message += format_exception(e)
					LOGE(message)
					self.current_workflow.update.message.reply_text(f"Error: {message}")
				LOGI(f"CI workflow finished, project: {workflow_name}")
				self.current_workflow = None
			except Exception as e:
				message = "Unhandled exception from QueueManager:"
				message += format_exception(e)
				LOGE(message)

	def put(self, workflow):
		self.queue.put(workflow)

	def get_queue_list(self):
		with self.queue.mutex:
			return list(self.queue.queue)

	def get_formatted_queue_list(self):
		qsize = self.queue.qsize()
		workflows_info = []
		for i, workflow in enumerate(self.get_queue_list()):
			workflows_info += [f"{i+1}) {workflow.get_info()}"]
		running = self.current_workflow is not None
		text = f"CI status: {'Running' if running else 'Stopped'}\n\n"
		if running:
			text += f"Running workflow: {self.current_workflow.get_info()}\n"
		text += f"Queued workflows: {qsize}\n\n"
		text += "\n".join(workflows_info)
		return text

# Use a global queue, even for multiple bot instances
# since they will run on the same machine
queue_manager = QueueManager()
