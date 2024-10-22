DEFAULT_GOAL:  pythonanalysis

# install requirements
# chmod +x filename 
.PHONY: getreqs
getreqs:
	#pip install --upgrade -r reqs.txt
	#cd user_provided/kubios
	#git pull 
	#cd ../..
	#ls


# analyze the dataset
.PHONY: pythonanalysis
pythonanalysis: getreqs
	python3  code/python/main.py


# serve the local directory
.PHONY: web
web: pythonanalysis
	python3 -m http.server --directory docs/

# live at http://127.0.0.1:8000/
