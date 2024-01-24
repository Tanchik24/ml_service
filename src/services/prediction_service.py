from src.ml.MLModel import MLModel
import time
from datetime import datetime
import asyncio
from src.repositories.PredictionRepository import prediction_repository
from src.repositories.ModelRepository import model_repository
from rq import Queue, get_current_job
import uuid
from fastapi import BackgroundTasks
from redis import Redis
from src.ml.preprocess import CSVDataProcessor
from src.schemas.user import User
from src.schemas.predictor import PredictionResponse
from src.exceptions import ModelNotFoundError, JobNotFoundError
from src.schemas.predictor import PredictionInfo
import pandas as pd
import logging

redis_conn = Redis()


# class PredictionService:
#     def __init__(self):
#         self.jobs = {}
#         self.queue = asyncio.Queue()
#         self.model = MLModel()
#         self.data_preprocessor = CSVDataProcessor()
#
#     async def get_model_from_db(self, model):
#         model_info = await model_repository.get_by_modelname(modelname=model)
#         if model_info is None:
#             raise ModelNotFoundError()
#         return model_info
#
#     async def predict(self, background_tasks, user, model, file):
#         model_info = await self.get_model_from_db(model)
#         data = await self.data_preprocessor.process(file)
#         data_json = data.to_json()
#         model_dict = {'name': model_info.modelname, 'path': model_info.file_path, 'id': model_info.id}
#         job_id = str(uuid.uuid4())
#         create_time = time.time()
#         job_info = {
#             'model_info': model_dict,
#             'data': data_json,
#             'user_id': user.id,
#             'create_time': create_time
#         }
#         self.jobs[job_id] = job_info
#         await self.queue.put(job_id)
#         background_tasks.add_task(self.handle_prediction, job_id)
#
#         create_time = datetime.fromtimestamp(create_time)
#
#         prediction = PredictionInfo(id=job_id,
#                                 user_id=user.id,
#                                 model_id=model_info.id,
#                                 cost=model_info.cost,
#                                 timestamp=create_time)
#
#         await prediction_repository.add(prediction.dict())
#
#         return job_id
#
#     async def handle_prediction(self, job_id):
#         logging.info(f"Начинается обработка задачи с ID {job_id}")
#         print(f"Начинается обработка задачи с ID {job_id}")
#         while True:
#             current_job_id = await self.queue.get()
#             if current_job_id == job_id:
#                 break
#             await self.queue.put(current_job_id)
#             await asyncio.sleep(1)
#
#         job_info = self.jobs[job_id]
#         data = pd.read_json(job_info['data'])
#
#         start_time = time.time()
#
#         try:
#             print('выподняется предсказание')
#             prediction = self.model.get_prediction(job_info['model_info']['name'], job_info['model_info']['path'], data)
#             end_time = time.time()
#             duration = end_time - start_time
#
#             self.jobs[job_id]['result'] = prediction
#             self.jobs[job_id]['status'] = 'completed'
#             self.jobs[job_id]['duration'] = duration
#             print('все готово')
#             model_repository.update(job_id, {"is_successful": True, "duration": duration})
#         except Exception as e:
#             print('ошибка')
#             end_time = time.time()
#             duration = end_time - start_time
#
#             self.jobs[job_id]['status'] = 'failed'
#             self.jobs[job_id]['error'] = str(e)
#             self.jobs[job_id]['duration'] = duration
#
#             model_repository.update(job_id, {"is_successful": False, "duration": duration, "error": str(e)})
#         except Exception as e:
#             self.jobs[job_id]['status'] = 'failed'
#             self.jobs[job_id]['error'] = str(e)
#
#
#     def get_job_status(self, job_id):
#         job_info = self.jobs.get(job_id)
#         if not job_info:
#             raise JobNotFoundError()
#         print('статус работы' + ' ' + job_info['status'])
#
#         response = PredictionResponse(prediction_id=job_id, prediction_model_id=job_info['model_info']['id'], created_at=job_info['create_time'],
#                                       prediction_results=job_info['results'])
#
#         return response
#
#

class PredictionService:
    def __init__(self):
        self.queue = Queue(connection=redis_conn)
        self.model = MLModel()
        self.data_preprocessor = CSVDataProcessor()

    def get_all_models(self):
        all_models = model_repository.list_all()

    async def get_model_from_db(self, model):
        model_info = await model_repository.get_by_modelname(modelname=model)
        if model_info is None:
            raise ModelNotFoundError()
        return model_info

    async def predict(self, background_tasks: BackgroundTasks, user: User, model: str, file):
        model_info = await self.get_model_from_db(model)
        data = await self.data_preprocessor.process(file)
        data_json = data.to_json()
        model_dict = {'name': model_info.modelname, 'path': model_info.file_path, 'id': model_info.id}
        job = self.queue.enqueue(self.handle_prediction, args=(model_dict, data_json))
        background_tasks.add_task(self.check_job_status, job.id)
        create_time = time.time()
        prediction = PredictionResponse(id=job.id,
                   user_id=user.id,
                   model_id=model_info.id,
                   cost=model_info.cost,
                   timestamp=create_time)

        model_repository.add(prediction.dict())
        job.meta['time'] = create_time

        return job.id

    def handle_prediction(self, model_info, data):
        # job = self.queue.fetch_job(get_current_job().id)

        data = pd.read_json(data)

        start_time = time.time()

        try:
            prediction = self.model.get_prediction(model_info['name'], model_info['path'], data)
            total_time = time.time() - start_time

            # job.meta['model_id'] = model_info['id']
            # job.meta['result'] = prediction
            # job.meta['total_time'] = total_time
            # job.save_meta()
        except Exception as e:
            return None
            # job.meta['error'] = str(e)
            # job.save_meta()
        return {"model_id": model_info['id'], "results": prediction, "total_time": total_time}

    def check_job_status(self, job_id):
        job = self.queue.fetch_job(job_id)
        while not job.is_finished and not job.is_failed:
            time.sleep(1)
            job.refresh()

        if job.is_failed:
            model_repository.update(job.id, {"is_successful": False})
            job.meta['status'] = 'error'
            job.meta['message'] = job.meta.get('error', 'Unknown error')
        else:
            model_repository.update(job.id, {"is_successful": True, "duration": job.meta['total_time']})
            job.meta['status'] = 'completed'

        job.save_meta()

    def get_job_status(self, job_id):
        job = self.queue.fetch_job(job_id)
        if not job:
            raise JobNotFoundError()

        response = PredictionResponse(prediction_id=job.id, prediction_model_id=job.meta['model_id'], created_at=job.meta['time'],
                                      prediction_results=job.meta['result'])

        return response


prediction_service = PredictionService()
