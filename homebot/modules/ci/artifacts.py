from pathlib import Path

class _ArtifactStatus:
	(
		_ON_QUEUE,
		_UPLOADING,
		_SUCCESS,
		_ERROR,
	) = range(4)

	_STRINGS = {
		_ON_QUEUE: "On queue",
		_UPLOADING: "Uploading",
		_SUCCESS: "Uploaded",
		_ERROR: "Error while uploading",
	}

	def __init__(self, status):
		self.status = status
	
	def __int__(self):
		return self.status
	
	def __str__(self) -> str:
		return self._STRINGS[self.status]

class ArtifactStatus(_ArtifactStatus):
	ON_QUEUE = _ArtifactStatus(_ArtifactStatus._ON_QUEUE)
	UPLOADING = _ArtifactStatus(_ArtifactStatus._UPLOADING)
	SUCCESS = _ArtifactStatus(_ArtifactStatus._SUCCESS)
	ERROR = _ArtifactStatus(_ArtifactStatus._ERROR)

class Artifacts(dict):
	def __init__(self, path: Path, patterns: list[str]):
		"""Find the artifacts."""
		super().__init__()
		self.path = path
		self.patterns = patterns

	def update(self):
		self.clear()
		files = [list(self.path.glob(pattern)) for pattern in self.patterns]
		for artifact in [artifact for sublist in files for artifact in sublist]:
			self[artifact] = ArtifactStatus.ON_QUEUE

	def get_artifacts_on_status(self, status: ArtifactStatus):
		return [k for k, v in self.items() if v is status]

	def get_readable_artifacts_list(self):
		artifact_total = len(self)
		artifact_uploaded = len(self.get_artifacts_on_status(ArtifactStatus.SUCCESS))

		text = f"Uploaded {artifact_uploaded} out of {artifact_total} artifact(s)\n"
		for i, artifact in enumerate(self.keys(), 1):
			text += f"{i}) {artifact.name}: {self[artifact]}\n"
		return text
