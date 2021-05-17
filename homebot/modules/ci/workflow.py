from homebot.modules.ci.project import ProjectBase

class Workflow:
	def __init__(self, project: ProjectBase):
		"""Initialize the workflow."""
		self.project = project
		self.update = self.project.update
		self.context = self.project.context
		self.project_name = self.project.name
		self.starter = self.update.effective_user.name

	def run(self):
		return self.project.build()

	def get_info(self):
		return (f"{self.project_name}\n"
				f"Arguments: {' '.join(self.project.args)}\n"
				f"Started by: {self.starter}\n")
