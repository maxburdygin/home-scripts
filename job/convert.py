import json

# Ваш JSON
data = json.loads('{"text": " \u042d\u0442\u043e \u043d\u0430\u0437\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u00ab\u041b\u043e\u0432\u0443\u0448\u043a\u0430 \u0424\u0443\u043a\u0438\u0434\u0438\u0434\u0430\u00bb \u0438\u043b\u0438 \u00ab\u0413\u043e\u043f\u0441\u043e\u0432\u0430 \u0441\u043f\u0438\u0440\u0430\u043b\u044c \u043d\u0430\u0441\u0438\u043b\u0438\u044f\u00bb. \u0418\u043b\u0438 \u0432\u044b \u0435\u0449\u0451 \u0431\u043e\u043b\u0435\u0435 \u0437\u043d\u0430\u043a\u043e\u043c\u044b\u0445, \u0434\u043e\u0440\u043e\u0433\u0438\u043c \u0441\u043b\u0443\u0448\u0430\u0442\u0435\u043b\u044f\u043c, \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u0445. \u041f\u043e\u043c\u043d\u0438\u0442\u0435 \u0442\u0430\u043a\u0443\u044e \u043c\u0443\u0434\u0440\u043e\u0441\u0442\u044c? \u00ab\u0415\u0441\u043b\u0438 \u0434\u0440\u0430\u043a\u0430 \u043d\u0435\u0438\u0437\u0431\u0435\u0436\u043d\u0430, \u0431\u0435\u0439 \u043f\u0435\u0440\u0432\u044b\u043c\u00bb. \u0412\u043e\u0442 \u044d\u0442\u043e \u043e\u043d\u043e. \u0423 \u0432\u0430\u0441 \u0432 \u0432\u043e\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0438, \u0432\u0430\u043c \u0432\u0430\u0448\u0430 \u0432\u043e\u0442 \u044d\u0442\u0430 \u0440\u044b\u0436\u0430\u044f \u0441\u0432\u043e\u043b\u043e\u0447\u044c, \u0421\u0443\u0431\u0430\u0441\u0442\u043e\u0432\u044c\u044f, \u043f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0435\u0442 \u043d\u0435\u0438\u0437\u0431\u0435\u0436\u043d\u0443\u044e \u0434\u0440\u0430\u043a\u0443 \u0438 \u0433\u043e\u0432\u043e\u0440\u0438\u0442 \u00ab\u0414\u0440\u0430\u043a\u0430 \u043d\u0435\u0438\u0437\u0431\u0435\u0436\u043d\u0430, \u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u0431\u0435\u0439 \u043f\u0435\u0440\u0432\u044b\u043c\u00bb. \u041e \u0447\u0451\u043c \u044d\u0442\u043e \u043e\u043d\u0430 \u0442\u0430\u043a \u00ab\u043d\u0435\u0438\u0437\u0431\u0435\u0436\u043d\u0430\u00bb? \u0417\u043d\u0430\u0435\u0442\u0435 \u043f\u043e\u0447\u0435\u043c\u0443? \u0410 \u043f\u043e\u0442\u043e\u043c\u0443 \u0447\u0442\u043e \u0432\u044b \u0443\u0434\u0430\u0440\u0438\u043b\u0438. \u0412\u043e\u0442 \u0443\u0436\u0435 \u0438 \u0434\u0440\u0430\u043a\u0430. \u00ab\u041b\u043e\u0432\u0443\u0448\u043a\u0430 \u0424\u0443\u043a\u0438\u0434\u0438\u0434\u0430\u00bb \u2013 \u044d\u0442\u043e \u043d\u0430\u0447\u0430\u043b\u043e \u0432\u043e\u0439\u043d\u044b \u0438\u0437-\u0437\u0430 \u0442\u043e\u0433\u043e, \u0447\u0442\u043e \u0442\u044b \u0434\u0443\u043c\u0430\u0435\u0448\u044c, \u0447\u0442\u043e \u0442\u0432\u043e\u0439 \u043f\u0440\u043e\u0442\u0438\u0432\u043d\u0438\u043a \u0432\u043e\u043e\u0440\u0443\u0436\u0430\u0435\u0442\u0441\u044f. \u041f\u043e\u044d\u0442\u043e\u043c\u0443 \u0442\u044b \u043b\u0443\u0447\u0448\u0435 \u043d\u0430\u043f\u0430\u0434\u0451\u0448\u044c, \u043f\u043e\u043a\u0430 \u043e\u043d \u043d\u0435 \u0432\u043e\u043e\u0440\u0443\u0436\u0438\u043b\u0441\u044f \u0434\u043e \u0442\u0430\u043a\u043e\u0439 \u0441\u0442\u0435\u043f\u0435\u043d\u0438, \u0447\u0442\u043e\u0431\u044b \u043e\u043d \u0441\u0442\u0430\u043b \u0442\u0435\u0431\u044f \u0441\u0438\u043b\u044c\u043d\u0435\u0435. \u00ab\u0413\u043e\u043f\u0441\u043e\u0432\u0430 \u0441\u043f\u0438\u0440\u0430\u043b\u044c \u043d\u0430\u0441\u0438\u043b\u0438\u044f\u00bb \u2013 \u044d\u0442\u043e \u043d\u0430\u0441\u0438\u043b\u0438\u0435, \u0438\u0441\u0445\u043e\u0434\u044f \u0438\u0437 \u043f\u0440\u0435\u0434\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f, \u0447\u0442\u043e \u043a\u0442\u043e-\u0442\u043e \u0434\u0440\u0443\u0433\u043e\u0439 \u043f\u0440\u043e\u0442\u0438\u0432 \u0442\u0435\u0431\u044f \u0437\u043b\u043e\u0443\u043c\u044b\u0448\u043b\u044f\u0435\u0442, \u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u043b\u0443\u0447\u0448\u0435 \u0441\u0435\u0439\u0447\u0430\u0441. \u0410 \u0442\u044b \u043c\u043e\u043b\u043e\u0434\u0435\u0446 \u0442\u0430\u043a\u043e\u0439, \u0435\u0433\u043e \u0441\u0442\u0440\u0430\u0442\u0435\u0433 \u0432\u0435\u043b\u0438\u043a\u0438\u0439, \u0443\u0434\u0430\u0440\u0438\u043b \u043f\u0435\u0440\u0432\u044b\u043c, \u043f\u043e\u043b\u0443\u0447\u0438\u043b \u0432 \u043e\u0442\u0432\u0435\u0442 \u043f\u043e\u043b\u0431\u0443. \u0414\u0430\u043b\u044c\u0448\u0435 \u0433\u043e\u0432\u043e\u0440\u0438\u0448\u044c \u00ab\u0412\u043e\u0442 \u043a\u0430\u043a \u0436\u0435 \u044f \u0431\u044b\u043b \u043f\u0440\u0430\u0432, \u043e\u043d\u0438 \u0432\u0441\u0435\u0433\u0434\u0430 \u0445\u043e\u0442\u0435\u043b\u0438 \u043d\u0430\u0441 \u0432\u0441\u0435\u0445 \u0442\u0443\u0442 \u0438\u0437\u043d\u0438\u0447\u0442\u043e\u0436\u0438\u0442\u044c\u00bb. \u042d\u0442\u043e \u0443\u0436\u0430\u0441\u043d\u043e \u0441\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u043d\u043e. \u0418 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u043e \u043b\u044e\u0434\u0438 \u0441\u043e\u0432\u0435\u0440\u0448\u0430\u044e\u0442 \u0445\u0443\u0434\u0448\u0438\u0435 \u0441\u0432\u043e\u0438 \u043f\u043e\u0441\u0442\u0443\u043f\u043a\u0438. \u042d\u0442\u043e \u0436\u0435 \u043d\u0435 \u0434\u043b\u044f \u0442\u043e\u0433\u043e, \u0447\u0442\u043e\u0431\u044b \u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0447\u0435\u0433\u043e-\u0442\u043e, \u0430 \u0434\u043b\u044f \u0442\u043e\u0433\u043e, \u0447\u0442\u043e\u0431\u044b \u0447\u0435\u0433\u043e-\u0442\u043e \u0438\u0437\u0431\u0435\u0436\u0430\u0442\u044c. \u041d\u043e \u044d\u0442\u043e \u0447\u0435\u0433\u043e-\u0442\u043e, \u0447\u0435\u0433\u043e \u043e\u043d\u0438 \u0438\u0437\u0431\u0435\u0433\u0430\u044e\u0442. \u0418 \u043d\u0430\u043f\u0443\u0433\u0430\u043d\u043d\u044b\u0435 \u0447\u0435\u043c \u043e\u043d\u0438 \u0434\u0435\u043b\u0430\u044e\u0442 \u0442\u0430\u043a\u0438\u0435 \u0448\u0442\u0443\u043a\u0438, \u0447\u0443\u0434\u043e\u0432\u0438\u0449\u043d\u044b\u0435 \u0441\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u043d\u043e, \u0432\u0438\u0434\u043d\u044b \u0442\u043e\u043b\u044c\u043a\u043e \u0438\u043c \u0441\u0430\u043c\u0438\u043c. \u041e\u043f\u044f\u0442\u044c \u0436\u0435, \u0438\u0437 \u0440\u0430\u0441\u043f\u0440\u043e\u0441\u0442\u0440\u0430\u043d\u0451\u043d\u043d\u043e\u0433\u043e, \u0438\u0437, \u044f \u0431\u044b \u0441\u043a\u0430\u0437\u0430\u043b\u0430, \u043d\u0430\u0440\u043e\u0434\u043d\u043e\u0433\u043e. \u00ab\u0415\u0441\u043b\u0438 \u0431\u044b \u043c\u044b \u0441\u044e\u0434\u0430 \u043d\u0435 \u043f\u0440\u0438\u0448\u043b\u0438, \u0441\u044e\u0434\u0430 \u043f\u0440\u0438\u0448\u043b\u0438 \u0431\u044b \u0441\u043e\u043b\u0434\u0430\u0442\u044b \u041d\u0410\u0422\u041e\u00bb. \u0413\u0434\u0435 \u044d\u0442\u0438 \u0441\u043e\u043b\u0434\u0430\u0442\u044b \u041d\u0410\u0422\u041e? \u041f\u043e\u0447\u0435\u043c\u0443 \u043e\u043d\u0438 \u0441\u044e\u0434\u0430 \u043f\u0440\u0438\u0448\u043b\u0438 \u0431\u044b, \u0435\u0441\u043b\u0438 \u0431\u044b \u043c\u044b \u0441\u044e\u0434\u0430 \u043d\u0435 \u043f\u0440\u0438\u0448\u043b\u0438? \u041d\u0435\u043f\u043e\u043d\u044f\u0442\u043d\u043e. \u00ab\u041d\u043e \u043f\u043e\u0442\u043e\u043c \u043e\u043d\u0438 \u043f\u0440\u0438\u0434\u0443\u0442\u00bb, \u2013 \u0433\u043e\u0432\u043e\u0440\u044f\u0442 \u043d\u0430\u043c \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u044b \u043f\u043e \u043c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u043e\u043c\u0443 \u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u044e. \u041f\u043e\u0447\u0435\u043c\u0443? \u041f\u043e\u0442\u043e\u043c\u0443 \u0447\u0442\u043e \u043c\u044b \u0440\u0435\u0448\u0438\u043b\u0438 \u0434\u0435\u0439\u0441\u0442\u0432\u043e\u0432\u0430\u0442\u044c \u043d\u0430 \u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435. \u041d\u0430 \u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435 \u0447\u0435\u0433\u043e? \u041d\u0430 \u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432 \u0443 \u043d\u0430\u0441 \u0432 \u0433\u043e\u043b\u043e\u0432\u0435.", "segments": [{"id": 0, "seek": 0, "start": 0.0, "end": 6.0, "text": " \u042d\u0442\u043e \u043d\u0430\u0437\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u00ab\u041b\u043e\u0432\u0443\u0448\u043a\u0430 \u0424\u0443\u043a\u0438\u0434\u0438\u0434\u0430\u00bb \u0438\u043b\u0438 \u00ab\u0413\u043e\u043f\u0441\u043e\u0432\u0430 \u0441\u043f\u0438\u0440\u0430\u043b\u044c \u043d\u0430\u0441\u0438\u043b\u0438\u044f\u00bb.", "tokens": [50364, 6684, 40659, 4657, 14854, 1055, 34187, 13196, 10282, 3586, 435, 3444, 5933, 8101, 4657, 20784, 3762, 461, 13978, 5307, 4490, 3842, 6519, 5435, 681, 12513, 50664], "temperature": 0.0, "avg_logprob": -0.2242037127094884, "compression_ratio": 1.9560117302052786, "no_speech_prob": 0.02520972490310669}, {"id": 1, "seek": 0, "start": 6.0, "end": 10.0, "text": " \u0418\u043b\u0438 \u0432\u044b \u0435\u0449\u0451 \u0431\u043e\u043b\u0435\u0435 \u0437\u043d\u0430\u043a\u043e\u043c\u044b\u0445, \u0434\u043e\u0440\u043e\u0433\u0438\u043c \u0441\u043b\u0443\u0448\u0430\u0442\u0435\u043b\u044f\u043c, \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u0445.", "tokens": [50664, 34361, 2840, 13993, 15103, 40909, 7205, 11, 24365, 2165, 41839, 2134, 1414, 10531, 11, 21168, 919, 7861, 1157, 13, 50864], "temperature": 0.0, "avg_logprob": -0.2242037127094884, "compression_ratio": 1.9560117302052786, "no_speech_prob": 0.02520972490310669}, {"id": 2, "seek": 0, "start": 10.0, "end": 15.0, "text": " \u041f\u043e\u043c\u043d\u0438\u0442\u0435 \u0442\u0430\u043a\u0443\u044e \u043c\u0443\u0434\u0440\u043e\u0441\u0442\u044c? \u00ab\u0415\u0441\u043b\u0438 \u0434\u0440\u0430\u043a\u0430 \u043d\u0435\u0438\u0437\u0431\u0435\u0436\u043d\u0430, \u0431\u0435\u0439 \u043f\u0435\u0440\u0432\u044b\u043c\u00bb.", "tokens": [50864, 43030, 38066, 42456, 1084, 2955, 9938, 3167, 30, 4657, 10156, 5734, 37928, 39558, 1725, 5572, 1552, 6029, 1931, 11, 1268, 2345, 11922, 11250, 12513, 51114], "temperature": 0.0, "avg_logprob": -0.2242037127094884, "compression_ratio": 1.9560117302052786, "no_speech_prob": 0.02520972490310669}, {"id": 3, "seek": 0, "start": 15.0, "end": 17.0, "text": " \u0412\u043e\u0442 \u044d\u0442\u043e \u043e\u043d\u043e.", "tokens": [51114, 9756, 2691, 25369, 13, 51214], "temperature": 0.0, "avg_logprob": -0.2242037127094884, "compression_ratio": 1.9560117302052786, "no_speech_prob": 0.02520972490310669}, {"id": 4, "seek": 0, "start": 17.0, "end": 22.0, "text": " \u0423 \u0432\u0430\u0441 \u0432 \u0432\u043e\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0438, \u0432\u0430\u043c \u0432\u0430\u0448\u0430 \u0432\u043e\u0442 \u044d\u0442\u0430 \u0440\u044b\u0436\u0430\u044f \u0441\u0432\u043e\u043b\u043e\u0447\u044c, \u0421\u0443\u0431\u0430\u0441\u0442\u043e\u0432\u044c\u044f, \u043f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0435\u0442 \u043d\u0435\u0438\u0437\u0431\u0435\u0436\u043d\u0443\u044e \u0434\u0440\u0430\u043a\u0443", "tokens": [51214, 6523, 10655, 740, 7900, 37176, 15573, 11, 10448, 14536, 386, 5505, 21396, 22791, 1820, 4251, 4155, 1227, 27497, 11, 2933, 8893, 9941, 1055, 14195, 11, 34614, 3310, 1725, 5572, 1552, 6029, 9882, 37928, 1272, 585, 51464], "temperature": 0.0, "avg_logprob": -0.2242037127094884, "compression_ratio": 1.9560117302052786, "no_speech_prob": 0.02520972490310669}, {"id": 5, "seek": 0, "start": 22.0, "end": 26.0, "text": " \u0438 \u0433\u043e\u0432\u043e\u0440\u0438\u0442 \u00ab\u0414\u0440\u0430\u043a\u0430 \u043d\u0435\u0438\u0437\u0431\u0435\u0436\u043d\u0430, \u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u0431\u0435\u0439 \u043f\u0435\u0440\u0432\u044b\u043c\u00bb.", "tokens": [51464, 1006, 25083, 4657, 8442, 481, 39558, 1725, 5572, 1552, 6029, 1931, 11, 19698, 1268, 2345, 11922, 11250, 12513, 51664], "temperature": 0.0, "avg_logprob": -0.2242037127094884, "compression_ratio": 1.9560117302052786, "no_speech_prob": 0.02520972490310669}, {"id": 6, "seek": 0, "start": 26.0, "end": 28.0, "text": " \u041e \u0447\u0451\u043c \u044d\u0442\u043e \u043e\u043d\u0430 \u0442\u0430\u043a \u00ab\u043d\u0435\u0438\u0437\u0431\u0435\u0436\u043d\u0430\u00bb?", "tokens": [51664, 3688, 1358, 12868, 2691, 8826, 2936, 4657, 4677, 5572, 1552, 6029, 1931, 5933, 30, 51764], "temperature": 0.0, "avg_logprob": -0.2242037127094884, "compression_ratio": 1.9560117302052786, "no_speech_prob": 0.02520972490310669}, {"id": 7, "seek": 2800, "start": 28.0, "end": 32.0, "text": " \u0417\u043d\u0430\u0435\u0442\u0435 \u043f\u043e\u0447\u0435\u043c\u0443? \u0410 \u043f\u043e\u0442\u043e\u043c\u0443 \u0447\u0442\u043e \u0432\u044b \u0443\u0434\u0430\u0440\u0438\u043b\u0438. \u0412\u043e\u0442 \u0443\u0436\u0435 \u0438 \u0434\u0440\u0430\u043a\u0430.", "tokens": [50364, 30869, 10524, 21513, 30, 3450, 11919, 2143, 2840, 39047, 5435, 13, 9756, 7520, 1006, 37928, 39558, 13, 50564], "temperature": 0.0, "avg_logprob": -0.07793555294510222, "compression_ratio": 1.9657142857142857, "no_speech_prob": 0.004050903487950563}, {"id": 8, "seek": 2800, "start": 32.0, "end": 38.0, "text": " \u00ab\u041b\u043e\u0432\u0443\u0448\u043a\u0430 \u0424\u0443\u043a\u0438\u0434\u0438\u0434\u0430\u00bb \u2013 \u044d\u0442\u043e \u043d\u0430\u0447\u0430\u043b\u043e \u0432\u043e\u0439\u043d\u044b \u0438\u0437-\u0437\u0430 \u0442\u043e\u0433\u043e, \u0447\u0442\u043e \u0442\u044b \u0434\u0443\u043c\u0430\u0435\u0448\u044c, \u0447\u0442\u043e \u0442\u0432\u043e\u0439 \u043f\u0440\u043e\u0442\u0438\u0432\u043d\u0438\u043a \u0432\u043e\u043e\u0440\u0443\u0436\u0430\u0435\u0442\u0441\u044f.", "tokens": [50564, 4657, 14854, 1055, 34187, 13196, 10282, 3586, 435, 3444, 5933, 1662, 2691, 8970, 12441, 26055, 1834, 3943, 12, 18598, 11283, 11, 2143, 5991, 13082, 17266, 11, 2143, 1069, 37325, 22534, 9715, 7900, 1717, 5726, 6970, 13, 50864], "temperature": 0.0, "avg_logprob": -0.07793555294510222, "compression_ratio": 1.9657142857142857, "no_speech_prob": 0.004050903487950563}, {"id": 9, "seek": 2800, "start": 38.0, "end": 44.0, "text": " \u041f\u043e\u044d\u0442\u043e\u043c\u0443 \u0442\u044b \u043b\u0443\u0447\u0448\u0435 \u043d\u0430\u043f\u0430\u0434\u0451\u0448\u044c, \u043f\u043e\u043a\u0430 \u043e\u043d \u043d\u0435 \u0432\u043e\u043e\u0440\u0443\u0436\u0438\u043b\u0441\u044f \u0434\u043e \u0442\u0430\u043a\u043e\u0439 \u0441\u0442\u0435\u043f\u0435\u043d\u0438, \u0447\u0442\u043e\u0431\u044b \u043e\u043d \u0441\u0442\u0430\u043b \u0442\u0435\u0431\u044f \u0441\u0438\u043b\u044c\u043d\u0435\u0435.", "tokens": [50864, 22318, 5991, 21569, 9011, 2601, 2882, 18263, 11, 17770, 5345, 1725, 7900, 1717, 5726, 14260, 5865, 13452, 3266, 5018, 2495, 11, 7887, 5345, 28980, 12644, 34158, 15627, 13, 51164], "temperature": 0.0, "avg_logprob": -0.07793555294510222, "compression_ratio": 1.9657142857142857, "no_speech_prob": 0.004050903487950563}, {"id": 10, "seek": 2800, "start": 44.0, "end": 52.0, "text": " \u00ab\u0413\u043e\u043f\u0441\u043e\u0432\u0430 \u0441\u043f\u0438\u0440\u0430\u043b\u044c \u043d\u0430\u0441\u0438\u043b\u0438\u044f\u00bb \u2013 \u044d\u0442\u043e \u043d\u0430\u0441\u0438\u043b\u0438\u0435, \u0438\u0441\u0445\u043e\u0434\u044f \u0438\u0437 \u043f\u0440\u0435\u0434\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f, \u0447\u0442\u043e \u043a\u0442\u043e-\u0442\u043e \u0434\u0440\u0443\u0433\u043e\u0439 \u043f\u0440\u043e\u0442\u0438\u0432 \u0442\u0435\u0431\u044f \u0437\u043b\u043e\u0443\u043c\u044b\u0448\u043b\u044f\u0435\u0442,", "tokens": [51164, 4657, 20784, 3762, 461, 13978, 5307, 4490, 3842, 6519, 5435, 681, 5933, 1662, 2691, 6519, 5435, 387, 11, 12410, 5280, 681, 3943, 8048, 37251, 5332, 11, 2143, 12278, 12, 860, 27823, 22534, 12644, 1423, 4610, 5525, 12533, 2873, 1094, 11, 51564], "temperature": 0.0, "avg_logprob": -0.07793555294510222, "compression_ratio": 1.9657142857142857, "no_speech_prob": 0.004050903487950563}, {"id": 11, "seek": 2800, "start": 52.0, "end": 54.0, "text": " \u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u043b\u0443\u0447\u0448\u0435 \u0441\u0435\u0439\u0447\u0430\u0441.", "tokens": [51564, 19698, 21569, 10241, 13, 51664], "temperature": 0.0, "avg_logprob": -0.07793555294510222, "compression_ratio": 1.9657142857142857, "no_speech_prob": 0.004050903487950563}, {"id": 12, "seek": 5400, "start": 54.0, "end": 60.0, "text": " \u0410 \u0442\u044b \u043c\u043e\u043b\u043e\u0434\u0435\u0446 \u0442\u0430\u043a\u043e\u0439, \u0435\u0433\u043e \u0441\u0442\u0440\u0430\u0442\u0435\u0433 \u0432\u0435\u043b\u0438\u043a\u0438\u0439, \u0443\u0434\u0430\u0440\u0438\u043b \u043f\u0435\u0440\u0432\u044b\u043c, \u043f\u043e\u043b\u0443\u0447\u0438\u043b \u0432 \u043e\u0442\u0432\u0435\u0442 \u043f\u043e\u043b\u0431\u0443.", "tokens": [50364, 3450, 5991, 28801, 10935, 13452, 11, 6448, 3266, 11157, 4953, 740, 8334, 8583, 11, 39047, 2338, 11922, 11250, 11, 9478, 2338, 740, 25284, 4692, 33567, 13, 50664], "temperature": 0.0, "avg_logprob": -0.13294786913641568, "compression_ratio": 2.0678851174934727, "no_speech_prob": 0.2634311020374298}, {"id": 13, "seek": 5400, "start": 60.0, "end": 64.0, "text": " \u0414\u0430\u043b\u044c\u0448\u0435 \u0433\u043e\u0432\u043e\u0440\u0438\u0448\u044c \u00ab\u0412\u043e\u0442 \u043a\u0430\u043a \u0436\u0435 \u044f \u0431\u044b\u043b \u043f\u0440\u0430\u0432, \u043e\u043d\u0438 \u0432\u0441\u0435\u0433\u0434\u0430 \u0445\u043e\u0442\u0435\u043b\u0438 \u043d\u0430\u0441 \u0432\u0441\u0435\u0445 \u0442\u0443\u0442 \u0438\u0437\u043d\u0438\u0447\u0442\u043e\u0436\u0438\u0442\u044c\u00bb.", "tokens": [50664, 3401, 3842, 5246, 8180, 17860, 4657, 42262, 3014, 6151, 2552, 10059, 10615, 11, 7515, 19087, 11515, 8334, 6519, 17260, 12848, 3943, 27996, 403, 2161, 3258, 12513, 50864], "temperature": 0.0, "avg_logprob": -0.13294786913641568, "compression_ratio": 2.0678851174934727, "no_speech_prob": 0.2634311020374298}, {"id": 14, "seek": 5400, "start": 64.0, "end": 66.0, "text": " \u042d\u0442\u043e \u0443\u0436\u0430\u0441\u043d\u043e \u0441\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u043d\u043e.", "tokens": [50864, 6684, 44973, 1234, 37075, 13, 50964], "temperature": 0.0, "avg_logprob": -0.13294786913641568, "compression_ratio": 2.0678851174934727, "no_speech_prob": 0.2634311020374298}, {"id": 15, "seek": 5400, "start": 66.0, "end": 70.0, "text": " \u0418 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u043e \u043b\u044e\u0434\u0438 \u0441\u043e\u0432\u0435\u0440\u0448\u0430\u044e\u0442 \u0445\u0443\u0434\u0448\u0438\u0435 \u0441\u0432\u043e\u0438 \u043f\u043e\u0441\u0442\u0443\u043f\u043a\u0438.", "tokens": [50964, 3272, 27208, 15850, 26227, 6406, 48609, 35202, 25375, 43829, 2241, 13, 51164], "temperature": 0.0, "avg_logprob": -0.13294786913641568, "compression_ratio": 2.0678851174934727, "no_speech_prob": 0.2634311020374298}, {"id": 16, "seek": 5400, "start": 70.0, "end": 74.0, "text": " \u042d\u0442\u043e \u0436\u0435 \u043d\u0435 \u0434\u043b\u044f \u0442\u043e\u0433\u043e, \u0447\u0442\u043e\u0431\u044b \u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0447\u0435\u0433\u043e-\u0442\u043e, \u0430 \u0434\u043b\u044f \u0442\u043e\u0433\u043e, \u0447\u0442\u043e\u0431\u044b \u0447\u0435\u0433\u043e-\u0442\u043e \u0438\u0437\u0431\u0435\u0436\u0430\u0442\u044c.", "tokens": [51164, 6684, 6151, 1725, 5561, 11283, 11, 7887, 41725, 19275, 12, 860, 11, 2559, 5561, 11283, 11, 7887, 19275, 12, 860, 38995, 6029, 2209, 13, 51364], "temperature": 0.0, "avg_logprob": -0.13294786913641568, "compression_ratio": 2.0678851174934727, "no_speech_prob": 0.2634311020374298}, {"id": 17, "seek": 5400, "start": 74.0, "end": 76.0, "text": " \u041d\u043e \u044d\u0442\u043e \u0447\u0435\u0433\u043e-\u0442\u043e, \u0447\u0435\u0433\u043e \u043e\u043d\u0438 \u0438\u0437\u0431\u0435\u0433\u0430\u044e\u0442.", "tokens": [51364, 7264, 2691, 19275, 12, 860, 11, 19275, 7515, 38995, 4953, 6406, 13, 51464], "temperature": 0.0, "avg_logprob": -0.13294786913641568, "compression_ratio": 2.0678851174934727, "no_speech_prob": 0.2634311020374298}, {"id": 18, "seek": 5400, "start": 76.0, "end": 83.0, "text": " \u0418 \u043d\u0430\u043f\u0443\u0433\u0430\u043d\u043d\u044b\u0435 \u0447\u0435\u043c \u043e\u043d\u0438 \u0434\u0435\u043b\u0430\u044e\u0442 \u0442\u0430\u043a\u0438\u0435 \u0448\u0442\u0443\u043a\u0438, \u0447\u0443\u0434\u043e\u0432\u0438\u0449\u043d\u044b\u0435 \u0441\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u043d\u043e, \u0432\u0438\u0434\u043d\u044b \u0442\u043e\u043b\u044c\u043a\u043e \u0438\u043c \u0441\u0430\u043c\u0438\u043c.", "tokens": [51464, 3272, 9011, 22638, 40194, 12056, 7515, 48732, 20113, 5941, 13549, 2241, 11, 43332, 1055, 22280, 4970, 37075, 11, 6504, 1834, 9008, 7604, 5602, 2165, 13, 51814], "temperature": 0.0, "avg_logprob": -0.13294786913641568, "compression_ratio": 2.0678851174934727, "no_speech_prob": 0.2634311020374298}, {"id": 19, "seek": 8300, "start": 84.0, "end": 89.0, "text": " \u041e\u043f\u044f\u0442\u044c \u0436\u0435, \u0438\u0437 \u0440\u0430\u0441\u043f\u0440\u043e\u0441\u0442\u0440\u0430\u043d\u0451\u043d\u043d\u043e\u0433\u043e, \u0438\u0437, \u044f \u0431\u044b \u0441\u043a\u0430\u0437\u0430\u043b\u0430, \u043d\u0430\u0440\u043e\u0434\u043d\u043e\u0433\u043e.", "tokens": [50414, 45246, 8773, 6151, 11, 3943, 26588, 9938, 28484, 22212, 4699, 11, 3943, 11, 2552, 2768, 48179, 11, 32583, 4699, 13, 50664], "temperature": 0.0, "avg_logprob": -0.10605424558612662, "compression_ratio": 2.210526315789474, "no_speech_prob": 0.015992311760783195}, {"id": 20, "seek": 8300, "start": 89.0, "end": 92.0, "text": " \u00ab\u0415\u0441\u043b\u0438 \u0431\u044b \u043c\u044b \u0441\u044e\u0434\u0430 \u043d\u0435 \u043f\u0440\u0438\u0448\u043b\u0438, \u0441\u044e\u0434\u0430 \u043f\u0440\u0438\u0448\u043b\u0438 \u0431\u044b \u0441\u043e\u043b\u0434\u0430\u0442\u044b \u041d\u0410\u0422\u041e\u00bb.", "tokens": [50664, 4657, 10156, 5734, 2768, 4777, 25306, 1725, 22448, 1675, 11, 25306, 22448, 1675, 2768, 36059, 856, 32014, 44416, 8556, 7876, 12513, 50814], "temperature": 0.0, "avg_logprob": -0.10605424558612662, "compression_ratio": 2.210526315789474, "no_speech_prob": 0.015992311760783195}, {"id": 21, "seek": 8300, "start": 92.0, "end": 96.0, "text": " \u0413\u0434\u0435 \u044d\u0442\u0438 \u0441\u043e\u043b\u0434\u0430\u0442\u044b \u041d\u0410\u0422\u041e? \u041f\u043e\u0447\u0435\u043c\u0443 \u043e\u043d\u0438 \u0441\u044e\u0434\u0430 \u043f\u0440\u0438\u0448\u043b\u0438 \u0431\u044b, \u0435\u0441\u043b\u0438 \u0431\u044b \u043c\u044b \u0441\u044e\u0434\u0430 \u043d\u0435 \u043f\u0440\u0438\u0448\u043b\u0438?", "tokens": [50814, 41996, 11012, 36059, 856, 32014, 44416, 8556, 7876, 30, 32823, 7515, 25306, 22448, 1675, 2768, 11, 8042, 2768, 4777, 25306, 1725, 22448, 1675, 30, 51014], "temperature": 0.0, "avg_logprob": -0.10605424558612662, "compression_ratio": 2.210526315789474, "no_speech_prob": 0.015992311760783195}, {"id": 22, "seek": 8300, "start": 96.0, "end": 97.0, "text": " \u041d\u0435\u043f\u043e\u043d\u044f\u0442\u043d\u043e.", "tokens": [51014, 2410, 5018, 1784, 19005, 13, 51064], "temperature": 0.0, "avg_logprob": -0.10605424558612662, "compression_ratio": 2.210526315789474, "no_speech_prob": 0.015992311760783195}, {"id": 23, "seek": 8300, "start": 97.0, "end": 101.0, "text": " \u00ab\u041d\u043e \u043f\u043e\u0442\u043e\u043c \u043e\u043d\u0438 \u043f\u0440\u0438\u0434\u0443\u0442\u00bb, \u2013 \u0433\u043e\u0432\u043e\u0440\u044f\u0442 \u043d\u0430\u043c \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u044b \u043f\u043e \u043c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u043e\u043c\u0443 \u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u044e.", "tokens": [51064, 4657, 6371, 354, 16873, 7515, 21255, 3767, 21606, 1662, 33374, 11401, 25665, 36948, 698, 2801, 24098, 1931, 10004, 20109, 30708, 18830, 13, 51264], "temperature": 0.0, "avg_logprob": -0.10605424558612662, "compression_ratio": 2.210526315789474, "no_speech_prob": 0.015992311760783195}, {"id": 24, "seek": 8300, "start": 101.0, "end": 105.0, "text": " \u041f\u043e\u0447\u0435\u043c\u0443? \u041f\u043e\u0442\u043e\u043c\u0443 \u0447\u0442\u043e \u043c\u044b \u0440\u0435\u0448\u0438\u043b\u0438 \u0434\u0435\u0439\u0441\u0442\u0432\u043e\u0432\u0430\u0442\u044c \u043d\u0430 \u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435.", "tokens": [51264, 32823, 30, 23671, 2143, 4777, 14025, 5435, 17136, 14069, 1470, 16036, 481, 41979, 5627, 13, 51464], "temperature": 0.0, "avg_logprob": -0.10605424558612662, "compression_ratio": 2.210526315789474, "no_speech_prob": 0.015992311760783195}, {"id": 25, "seek": 8300, "start": 105.0, "end": 109.0, "text": " \u041d\u0430 \u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435 \u0447\u0435\u0433\u043e? \u041d\u0430 \u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432 \u0443 \u043d\u0430\u0441 \u0432 \u0433\u043e\u043b\u043e\u0432\u0435.", "tokens": [51464, 11245, 16036, 481, 41979, 5627, 19275, 30, 11245, 16036, 481, 41979, 5627, 42390, 1055, 1595, 6519, 740, 24721, 387, 13, 51664], "temperature": 0.0, "avg_logprob": -0.10605424558612662, "compression_ratio": 2.210526315789474, "no_speech_prob": 0.015992311760783195}], "language": "Russian"}')
print(data)
# Конвертировать текст
text = data["text"].encode('utf-8').decode('unicode_escape')
print(text)