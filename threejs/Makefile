.PHONY: threejs
threejs:
	wget 'http://threejs.org/build/three.min.js' -O 'three.js'

.PHONY: audio
audio: models/mmd/audios/wavefile_short.mp3
	wget 'https://github.com/mrdoob/three.js/blob/dev/examples/models/mmd/audios/wavefile_short.mp3?raw=true' -O 'models/mmd/audios/wavefile_short.mp3'

.PHONY: camera
camera: models/mmd/vmds/wavefile_camera.vmd
	wget 'https://github.com/mrdoob/three.js/blob/dev/examples/models/mmd/vmds/wavefile_camera.vmd?raw=true' -O 'models/mmd/vmds/wavefile_camera.vmd'

.PHONY: models
models: models/mmd/miku/eyeM2.bmp models/mmd/miku/miku_v2.pmd
	wget 'https://github.com/mrdoob/three.js/blob/dev/examples/models/mmd/miku/eyeM2.bmp?raw=true' -O 'models/mmd/miku/eyeM2.bmp'
	wget 'https://github.com/mrdoob/three.js/blob/dev/examples/models/mmd/miku/miku_v2.pmd?raw=true' -O 'models/mmd/miku/miku_v2.pmd'

.PHONY: run
run: threejs audio camera models
	python3 -m http.server 7999

