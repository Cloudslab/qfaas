from typing import Optional, Dict

from pydantic import BaseModel, Field


class FunctionCodeSchema(BaseModel):
    requirements: Optional[str] = None
    handlerPy: str = Field(...)
    handlerQs: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "handlerPy": "base64(source_code_Python)",
                "handlerQs": "base64(source_code_QSharp)",
                "requirements": "base64(requirements)",
            }
        }


class FunctionSchema(BaseModel):
    name: str = Field(...)
    template: str = Field(...)
    fnCode: FunctionCodeSchema = Field(...)
    author: str = None
    public: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "qrng-aio",
                "template": "qiskit",
                "fnCode": {
                    "requirements": "",
                    "handlerPy": "ZnJvbSBxaXNraXQgaW1wb3J0ICoKZnJvbSBxaXNraXQucHJvdmlkZXJzLmlibXEgaW1wb3J0IGxlYXN0X2J1c3kKaW1wb3J0IGpzb24KCiMgU2FtcGxlIEpTT04gZm9ybWF0IGZvciBpbnB1dApzYW1wbGVJbnB1dCA9IHsKICAiaW5wdXQiOiAiPG51bWJlciBvZiBxdWJpdHMsIGZyb20gMSB0byA2NT4iLAogICJwcm92aWRlciI6ICI8cHJvdmlkZXIgKHFhc21fc2ltdWxhdG9yLCBpYm1xKT4iLAogICJzaG90cyI6ICI8bnVtYmVyIG9mIHNob3RzLCBkZWZhdWx0IGlzIDE+IiwKICAiYmFja2VuZF9pbmZvIjogewogICAgICAiaHViIjogIjxpYm1xX2h1Yl9uYW1lPiIsCiAgICAgICJhcGlfdG9rZW4iOiAiPGlibXFfYXBpX3Rva2VuPiIsCiAgICAgICJkZXZpY2UiOiAiPGJhY2tlbmRfbmFtZT4iLAogICAgICAiYXV0b3NlbGVjdCI6ICI8MCB0byBtYW51YWxseSBzZWxlY3QgdGhlIGRldmljZSBhYm92ZSwgMSB0byBzZWxlY3QgbGVhc3QgYnVzeSBtYWNoaW5lPiIKICB9Cn0KCiMgRXJyb3Igbm90aWNlcwpwcm92aWRlckVycm9yID0gIkVycm9yLiBUaGlzIGZ1bmN0aW9uIG9ubHkgc3VwcG9ydCBzaW11bGF0b3IgcHJvdmlkZXIgYXQgdGhlIG1vbWVudC4gUGxlYXNlIHRyeSBhZ2FpbiIKaW5wdXRFcnJvciA9ICJJbnZhbGlkIGlucHV0IGZvcm1hdC4gUGxlYXNlIHVzZSB0aGUgZm9sbG93aW5nIEpTT04gZm9ybWF0IGZvciBpbnB1dCBkYXRhIgoKCmRlZiBnZW5lcmF0ZVJlc3BvbnNlKHN0YXR1c0NvZGUsIGJvZHkpOgogIHJldHVybiB7CiAgICAic3RhdHVzQ29kZSI6IHN0YXR1c0NvZGUsCiAgICAiYm9keSI6IGJvZHkKICB9CgpkZWYgZ2VuZXJhdGVFcnJvcihzdGF0dXNDb2RlLCBlcnJvciwgZGV0YWlsKToKICByZXR1cm4gewogICAgInN0YXR1c0NvZGUiOiBzdGF0dXNDb2RlLAogICAgImJvZHkiOiB7CiAgICAgICJlcnJvciI6IHN0cihzdGF0dXNDb2RlKSArICIgLSAiICsgZXJyb3IsCiAgICAgICJkZXRhaWwiOiBkZXRhaWwsCiAgICAgICJzYW1wbGVfaW5wdXRfZm9ybWF0Ijogc2FtcGxlSW5wdXQKICAgIH0KICB9CgoKIyBHZXQgQVBJIHRva2VuIGZyb20gU2VjcmV0CmRlZiBnZXRBUElTZWNyZXQoc2VjcmV0TmFtZSk6CiAgICBzZWNyZXQgPSBvcGVuKCIvdmFyL29wZW5mYWFzL3NlY3JldHMvIiArIHNlY3JldE5hbWUsICJyIikucmVhZCgpCiAgICByZXR1cm4gc2VjcmV0CgojIEdlbmVyYXRlIFF1YW50dW0gQ2lyY3VpdApkZWYgZ2VuZXJhdGVDaXJjdWl0KGlucHV0KToKICAgICMgQ3JlYXRlIGNpcmN1aXQKICAgIHFyID0gUXVhbnR1bVJlZ2lzdGVyKGlucHV0LCAncScpCiAgICBjciA9IENsYXNzaWNhbFJlZ2lzdGVyKGlucHV0LCAnY3InKQogICAgY2lyY3VpdCA9IFF1YW50dW1DaXJjdWl0KHFyLCBjcikKICAgIGNpcmN1aXQuaChxcikKICAgIGNpcmN1aXQubWVhc3VyZShxciwgY3IpCiAgICByZXR1cm4gY2lyY3VpdAoKIyBHZXQgYmFja2VuZApkZWYgZ2V0QmFja2VuZChpbnB1dCwgcHJvdmlkZXIsIGJhY2tlbmRfaW5mbyk6CiAgICBiYWNrZW5kID0gTm9uZQogICAgaWYgcHJvdmlkZXIgPT0gJ3NpbXVsYXRvcic6CiAgICAgICAgYmFja2VuZCA9IEFlci5nZXRfYmFja2VuZCgncWFzbV9zaW11bGF0b3InKQoKICAgIGVsaWYgcHJvdmlkZXIgPT0gJ2libXEnOgogICAgICAgICMgTG9hZCBBUEkgdG9rZW4gKGRlZmF1bHQgZ2V0IGZyb20gc2VjcmV0KQogICAgICAgIGFwaV90b2tlbiA9IGJhY2tlbmRfaW5mby5nZXQoJ2FwaV90b2tlbicsIGdldEFQSVNlY3JldCgiaWJtLXRva2VuLWhvYW1iIikpCiAgICAgICAgaWYgYXBpX3Rva2VuID09ICIiOgogICAgICAgICAgICBhcGlfdG9rZW4gPSBnZXRBUElTZWNyZXQoImlibS10b2tlbi1ob2FtYiIpCiAgICAgICAgSUJNUS5zYXZlX2FjY291bnQoYXBpX3Rva2VuKQogICAgICAgIHByb3ZpZGVyID0gSUJNUS5sb2FkX2FjY291bnQoKQogICAgICAgICMgRGVmYXVsdCBwcm92aWRlciA9IGlibS1xLCBncm91cD0idW5pbWVsYiIsIHByb2plY3Q9InJlc2VhcmNoZXJzIgogICAgICAgIHByb3ZpZGVyID0gSUJNUS5nZXRfcHJvdmlkZXIoaHViPWJhY2tlbmRfaW5mby5nZXQoImh1YiIsICJpYm0tcSIpKQogICAgICAgICMgU2VsZWN0IGRldmljZSBhdXRvbWF0aWNhbGx5IChsZWFzdCBidXN5IGRldmljZSkgb3IgbWFudWFsbHkKICAgICAgICBpZihiYWNrZW5kX2luZm8uZ2V0KCJhdXRvc2VsZWN0IiwgVHJ1ZSkgPT0gVHJ1ZSk6CiAgICAgICAgICAgICMgU2VsZWN0IGF0IGxlYXN0IGJ1c3kgZGV2aWNlIChub3Qgc2ltdWxhdG9yKQogICAgICAgICAgICBiYWNrZW5kID0gbGVhc3RfYnVzeShwcm92aWRlci5iYWNrZW5kcyhmaWx0ZXJzPWxhbWJkYSB4OiB4LmNvbmZpZ3VyYXRpb24oKS5uX3F1Yml0cyA+PSBpbnB1dCBcCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFuZCBub3QgeC5jb25maWd1cmF0aW9uKCkuc2ltdWxhdG9yIGFuZCB4LnN0YXR1cygpLm9wZXJhdGlvbmFsPT1UcnVlKSkKICAgICAgICBlbHNlOiAKICAgICAgICAgICAgYmFja2VuZCA9IHByb3ZpZGVyLmdldF9iYWNrZW5kKGJhY2tlbmRfaW5mby5nZXQoImRldmljZSIpKQogICAgcmV0dXJuIGJhY2tlbmQKCiMgU3VibWl0IGpvYgpkZWYgc3VibWl0Sm9iKGNpcmN1aXQsIGJhY2tlbmQsIHNob3RzKToKICAgICMgRXhlY3V0ZSBqb2IKICAgIGpvYiA9IGV4ZWN1dGUoY2lyY3VpdCwgYmFja2VuZCwgc2hvdHM9c2hvdHMpCiAgICByZXR1cm4gam9iCgoKZGVmIHBvc3RfcHJvY2VzcyhyZXN1bHQpOgogICAgY291bnRzID0gcmVzdWx0LmdldF9jb3VudHMoKQogICAgcmV0dXJuIGNvdW50cwoKZGVmIGlzX2pzb24obXlqc29uKToKICB0cnk6CiAgICBqc29uLmxvYWRzKG15anNvbikKICBleGNlcHQ6CiAgICByZXR1cm4gRmFsc2UKICByZXR1cm4gVHJ1ZQoKZGVmIGhhbmRsZShldmVudCwgY29udGV4dCk6CiAgICBpZiBpc19qc29uKGV2ZW50LmJvZHkpPT1UcnVlOgogICAgICAgIHRyeToKICAgICAgICAgICAgaW5wdXQgPSBldmVudC5qc29uLmdldCgnaW5wdXQnKQogICAgICAgICAgICBwcm92aWRlciA9IGV2ZW50Lmpzb24uZ2V0KCdwcm92aWRlcicpCiAgICAgICAgICAgIHNob3RzID0gZXZlbnQuanNvbi5nZXQoJ3Nob3RzJykKICAgICAgICAgICAgYmFja2VuZF9pbmZvID0gZXZlbnQuanNvbi5nZXQoJ2JhY2tlbmRfaW5mbycpCiAgICAgICAgICAgIHdhaXQgPSBldmVudC5qc29uLmdldCgnd2FpdF9mb3JfcmVzdWx0JykKICAgICAgICBleGNlcHQ6CiAgICAgICAgICAgIHJldHVybiBnZW5lcmF0ZUVycm9yKDQwMCwgIkludmFsaWQgSW5wdXQiLCBpbnB1dEVycm9yKQogICAgICAgIGJhY2tlbmQgPSBnZXRCYWNrZW5kKGlucHV0LCBwcm92aWRlciwgYmFja2VuZF9pbmZvKQogICAgICAgIGlmIHN0cihpbnB1dCkuaXNudW1lcmljKCkgYW5kIDAgPCBpbnQoaW5wdXQpIDw9IDY1IGFuZCBiYWNrZW5kICE9IE5vbmU6CiAgICAgICAgICAgIGNpcmN1aXQgPSBnZW5lcmF0ZUNpcmN1aXQoaW5wdXQpCiAgICAgICAgICAgIGlmKHdhaXQgPT0gVHJ1ZSk6CiAgICAgICAgICAgICAgICBqb2IgPSBzdWJtaXRKb2IoY2lyY3VpdCwgYmFja2VuZCwgc2hvdHMpCiAgICAgICAgICAgICAgICByZXN1bHQgPSBwb3N0X3Byb2Nlc3Moam9iLnJlc3VsdCgpKQogICAgICAgICAgICAgICAgcHJvdmlkZXJfaW5mbyA9ICIiCiAgICAgICAgICAgICAgICBpZiBwcm92aWRlciA9PSAnaWJtcSc6IAogICAgICAgICAgICAgICAgICAgIGpvYl9pZCA9IGpvYi5qb2JfaWQoKQogICAgICAgICAgICAgICAgICAgIHRpbWVfc3RlcHMgPSBqb2IudGltZV9wZXJfc3RlcCgpCiAgICAgICAgICAgICAgICAgICAgcnVudGltZSA9IHRpbWVfc3RlcHNbIkNPTVBMRVRFRCJdIC0gdGltZV9zdGVwc1siUlVOTklORyJdCiAgICAgICAgICAgICAgICAgICAgZXhlY3V0aW9uX3RpbWUgPSBqb2IucmVzdWx0KCkudGltZV90YWtlbgogICAgICAgICAgICAgICAgICAgIHByb3ZpZGVyX2luZm8gPSB7IAogICAgICAgICAgICAgICAgICAgICAgICAic2hvdHMiOiByZXN1bHQuc2hvdHMoKSwKICAgICAgICAgICAgICAgICAgICAgICAgImpvYl9pZCI6IGpvYl9pZCwKICAgICAgICAgICAgICAgICAgICAgICAgImpvYl9zdGF0dXMiOiBzdHIoam9iLnN0YXR1cygpKSwKICAgICAgICAgICAgICAgICAgICAgICAgInJ1bm5pbmdfc3RhcnRfdGltZSI6IHN0cih0aW1lX3N0ZXBzWyJSVU5OSU5HIl0pLAogICAgICAgICAgICAgICAgICAgICAgICAiY29tcGxldGlvbl90aW1lIjogc3RyKHRpbWVfc3RlcHNbIkNPTVBMRVRFRCJdKSwKICAgICAgICAgICAgICAgICAgICAgICAgInRvdGFsX3J1bl90aW1lIjogcnVudGltZS50b3RhbF9zZWNvbmRzKCksCiAgICAgICAgICAgICAgICAgICAgICAgICJleGVjdXRpb25fdGltZSI6IGV4ZWN1dGlvbl90aW1lCiAgICAgICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIGpzb25fcmVzcG9uc2UgPSB7CiAgICAgICAgICAgICAgICAgICAgInJlc3VsdCI6IGludChtYXgocmVzdWx0LCBrZXk9cmVzdWx0LmdldCksMiksCiAgICAgICAgICAgICAgICAgICAgImJhY2tlbmRfZGV2aWNlIjogc3RyKGJhY2tlbmQpLAogICAgICAgICAgICAgICAgICAgICJkZXRhaWwiOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICJwcm92aWRlcl9pbmZvIjogcHJvdmlkZXJfaW5mbywKICAgICAgICAgICAgICAgICAgICAgICAgInJhbmRvbV9udW1iZXJfYmluYXJ5IjogbWF4KHJlc3VsdCwga2V5PXJlc3VsdC5nZXQpLAogICAgICAgICAgICAgICAgICAgICAgICAiY291bnRzIjogbWF4KHJlc3VsdC52YWx1ZXMoKSksCiAgICAgICAgICAgICAgICAgICAgICAgICJhbGxfcG9zc2libGVfdmFsdWVzIjoge2s6IGludChrLDIpIGZvciBrLHYgaW4gcmVzdWx0Lml0ZW1zKCkgaWYgdiA9PSBtYXgocmVzdWx0LnZhbHVlcygpKX0KICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICByZXR1cm4gZ2VuZXJhdGVSZXNwb25zZSgyMDAsanNvbl9yZXNwb25zZSkKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIGpvYiA9IHN1Ym1pdEpvYihjaXJjdWl0LCBiYWNrZW5kLCBzaG90cykKICAgICAgICAgICAgICAgIGpvYi5yZWZyZXNoKCkKICAgICAgICAgICAgICAgIGpzb25fcmVzcG9uc2UgPSB7CiAgICAgICAgICAgICAgICAgICAgImpvYl9pZCI6IHN0cihqb2Iuam9iX2lkKCkpLAogICAgICAgICAgICAgICAgICAgICJodWIiOiBiYWNrZW5kX2luZm8uZ2V0KCJodWIiKSwKICAgICAgICAgICAgICAgICAgICAiYmFja2VuZCI6IHN0cihiYWNrZW5kKSwKICAgICAgICAgICAgICAgICAgICAiam9iX3N1Ym1pdHRlZF90aW1lIjogc3RyKGpvYi5jcmVhdGlvbl9kYXRlKCkpICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgcmV0dXJuIGdlbmVyYXRlUmVzcG9uc2UoMjAwLGpzb25fcmVzcG9uc2UpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgcmV0dXJuIGdlbmVyYXRlRXJyb3IoNDAwLCAiSW52YWxpZCBJbnB1dCIsIGlucHV0RXJyb3IpCiAgICBlbHNlOgogICAgICAgICAgICByZXR1cm4gZ2VuZXJhdGVFcnJvcig0MDAsICJJbnZhbGlkIElucHV0IiwgaW5wdXRFcnJvcikK",
                    "handlerQs": "",
                },
                "public": 0,
            }
        }


class FunctionInvocationSchema(BaseModel):
    input: int = Field(...)
    shots: int = Field(...)
    waitForResult: bool = Field(...)
    provider: str = Field(...)
    autoSelect: bool = Field(...)
    backendType: Optional[str]
    backendName: Optional[str] = ""
    postProcessOnly: Optional[bool] = False
    jobRawResult: Optional[dict]
    jobId: Optional[str]
    local: Optional[bool] = 0

    class Config:
        schema_extra = {
            "example": {
                "input": 10,
                "shots": 10,
                "waitForResult": 1,
                "provider": "qfaas",
                "autoSelect": 0,
                "backendType": "simulator",
                "backendName": "",
                "local": 1,
            }
        }


class UpdateFunctionModel(BaseModel):
    name: str = Field(...)
    fnCode: Optional[FunctionCodeSchema]
    public: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "random-number",
                "fnCode": {
                    "requirements": "",
                    "handlerPy": "ZnJvbSBxaXNraXQgaW1wb3J0ICoKZnJvbSBxaXNraXQucHJvdmlkZXJzLmlibXEgaW1wb3J0IGxlYXN0X2J1c3kKaW1wb3J0IGpzb24KCiMgU2FtcGxlIEpTT04gZm9ybWF0IGZvciBpbnB1dApqc29uX2Zvcm1hdCA9IHsKICAiaW5wdXQiOiAiPG51bWJlciBvZiBxdWJpdHMsIGZyb20gMSB0byA2NT4iLAogICJwcm92aWRlciI6ICI8cHJvdmlkZXIgKHFhc21fc2ltdWxhdG9yLCBpYm1xKT4iLAogICJzaG90cyI6ICI8bnVtYmVyIG9mIHNob3RzLCBkZWZhdWx0IGlzIDE+IiwKICAiYmFja2VuZF9pbmZvIjogewogICAgICAiaHViIjogIjxpYm1xX2h1Yl9uYW1lPiIsCiAgICAgICJhcGlfdG9rZW4iOiAiPGlibXFfYXBpX3Rva2VuPiIsCiAgICAgICJkZXZpY2UiOiAiPGJhY2tlbmRfbmFtZT4iLAogICAgICAiYXV0b3NlbGVjdCI6ICI8MCB0byBtYW51YWxseSBzZWxlY3QgdGhlIGRldmljZSBhYm92ZSwgMSB0byBzZWxlY3QgbGVhc3QgYnVzeSBtYWNoaW5lPiIKICB9Cn0KCiMgR2V0IEFQSSB0b2tlbiBmcm9tIFNlY3JldApkZWYgZ2V0QVBJU2VjcmV0KHNlY3JldE5hbWUpOgogICAgc2VjcmV0ID0gb3BlbigiL3Zhci9vcGVuZmFhcy9zZWNyZXRzLyIgKyBzZWNyZXROYW1lLCAiciIpLnJlYWQoKQogICAgcmV0dXJuIHNlY3JldAoKIyBHZW5lcmF0ZSBRdWFudHVtIENpcmN1aXQKZGVmIGdlbmVyYXRlQ2lyY3VpdChpbnB1dCk6CiAgICAjIENyZWF0ZSBjaXJjdWl0CiAgICBxciA9IFF1YW50dW1SZWdpc3RlcihpbnB1dCwgJ3EnKQogICAgY3IgPSBDbGFzc2ljYWxSZWdpc3RlcihpbnB1dCwgJ2NyJykKICAgIGNpcmN1aXQgPSBRdWFudHVtQ2lyY3VpdChxciwgY3IpCiAgICBjaXJjdWl0LmgocXIpCiAgICBjaXJjdWl0Lm1lYXN1cmUocXIsIGNyKQogICAgcmV0dXJuIGNpcmN1aXQKCiMgR2V0IGJhY2tlbmQKZGVmIGdldEJhY2tlbmQoaW5wdXQsIHByb3ZpZGVyLCBiYWNrZW5kX2luZm8pOgogICAgYmFja2VuZCA9IE5vbmUKICAgIGlmIHByb3ZpZGVyID09ICdzaW11bGF0b3InOgogICAgICAgIGJhY2tlbmQgPSBBZXIuZ2V0X2JhY2tlbmQoJ3Fhc21fc2ltdWxhdG9yJykKCiAgICBlbGlmIHByb3ZpZGVyID09ICdpYm1xJzoKICAgICAgICAjIExvYWQgQVBJIHRva2VuIChkZWZhdWx0IGdldCBmcm9tIHNlY3JldCkKICAgICAgICBhcGlfdG9rZW4gPSBiYWNrZW5kX2luZm8uZ2V0KCdhcGlfdG9rZW4nLCBnZXRBUElTZWNyZXQoImlibS10b2tlbi1ob2FtYiIpKQogICAgICAgIGlmIGFwaV90b2tlbiA9PSAiIjoKICAgICAgICAgICAgYXBpX3Rva2VuID0gZ2V0QVBJU2VjcmV0KCJpYm0tdG9rZW4taG9hbWIiKQogICAgICAgIElCTVEuc2F2ZV9hY2NvdW50KGFwaV90b2tlbikKICAgICAgICBwcm92aWRlciA9IElCTVEubG9hZF9hY2NvdW50KCkKICAgICAgICAjIFNlbGVjdCBkZXZpY2UgYXV0b21hdGljYWxseSAobGVhc3QgYnVzeSBkZXZpY2UpIG9yIG1hbnVhbGx5CiAgICAgICAgaWYoYmFja2VuZF9pbmZvLmdldCgiYXV0b3NlbGVjdCIsIFRydWUpID09IFRydWUpOgogICAgICAgICAgICAjIERlZmF1bHQgcHJvdmlkZXIgPSBpYm0tcQogICAgICAgICAgICBwcm92aWRlciA9IElCTVEuZ2V0X3Byb3ZpZGVyKGh1Yj1iYWNrZW5kX2luZm8uZ2V0KCJodWIiLCAiaWJtLXEiKSkKICAgICAgICAgICAgIyBTZWxlY3QgYXQgbGVhc3QgYnVzeSBkZXZpY2UgKG5vdCBzaW11bGF0b3IpCiAgICAgICAgICAgIGJhY2tlbmQgPSBsZWFzdF9idXN5KHByb3ZpZGVyLmJhY2tlbmRzKGZpbHRlcnM9bGFtYmRhIHg6IHguY29uZmlndXJhdGlvbigpLm5fcXViaXRzID49IGlucHV0IFwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYW5kIG5vdCB4LmNvbmZpZ3VyYXRpb24oKS5zaW11bGF0b3IgYW5kIHguc3RhdHVzKCkub3BlcmF0aW9uYWw9PVRydWUpKQogICAgICAgIGVsc2U6IAogICAgICAgICAgICBiYWNrZW5kID0gcHJvdmlkZXIuZ2V0X2JhY2tlbmQoYmFja2VuZF9pbmZvLmdldCgiZGV2aWNlIikpCiAgICByZXR1cm4gYmFja2VuZAoKIyBTdWJtaXQgam9iCmRlZiBzdWJtaXRKb2IoY2lyY3VpdCwgYmFja2VuZCwgc2hvdHMpOgogICAgIyBFeGVjdXRlIGpvYgogICAgam9iID0gZXhlY3V0ZShjaXJjdWl0LCBiYWNrZW5kLCBzaG90cz1zaG90cykKICAgIHJldHVybiBqb2IKCgpkZWYgcG9zdF9wcm9jZXNzKHJlc3VsdCk6CiAgICBjb3VudHMgPSByZXN1bHQuZ2V0X2NvdW50cygpCiAgICByZXR1cm4gY291bnRzCgpkZWYgaXNfanNvbihteWpzb24pOgogIHRyeToKICAgIGpzb24ubG9hZHMobXlqc29uKQogIGV4Y2VwdDoKICAgIHJldHVybiBGYWxzZQogIHJldHVybiBUcnVlCgpkZWYgaGFuZGxlKGV2ZW50LCBjb250ZXh0KToKICAgIGlmIGlzX2pzb24oZXZlbnQuYm9keSk9PVRydWU6CiAgICAgICAgaW5wdXQgPSBldmVudC5qc29uLmdldCgnaW5wdXQnKQogICAgICAgIHByb3ZpZGVyID0gZXZlbnQuanNvbi5nZXQoJ3Byb3ZpZGVyJykKICAgICAgICBzaG90cyA9IGV2ZW50Lmpzb24uZ2V0KCdzaG90cycpCiAgICAgICAgYmFja2VuZF9pbmZvID0gZXZlbnQuanNvbi5nZXQoJ2JhY2tlbmRfaW5mbycpCiAgICAgICAgd2FpdCA9IGV2ZW50Lmpzb24uZ2V0KCd3YWl0X2Zvcl9yZXN1bHQnKQogICAgICAgIGJhY2tlbmQgPSBnZXRCYWNrZW5kKGlucHV0LCBwcm92aWRlciwgYmFja2VuZF9pbmZvKQoKICAgICAgICBpZiBzdHIoaW5wdXQpLmlzbnVtZXJpYygpIGFuZCAwIDwgaW50KGlucHV0KSA8PSA2NSBhbmQgYmFja2VuZCAhPSBOb25lOgogICAgICAgICAgICBjaXJjdWl0ID0gZ2VuZXJhdGVDaXJjdWl0KGlucHV0KQogICAgICAgICAgICBpZih3YWl0ID09IFRydWUpOgogICAgICAgICAgICAgICAgam9iID0gc3VibWl0Sm9iKGNpcmN1aXQsIGJhY2tlbmQsIHNob3RzKQogICAgICAgICAgICAgICAgcmVzdWx0ID0gcG9zdF9wcm9jZXNzKGpvYi5yZXN1bHQoKSkKICAgICAgICAgICAgICAgIHByb3ZpZGVyX2luZm8gPSAiIgogICAgICAgICAgICAgICAgaWYgcHJvdmlkZXIgPT0gJ2libXEnOiAKICAgICAgICAgICAgICAgICAgICBqb2JfaWQgPSBqb2Iuam9iX2lkKCkKICAgICAgICAgICAgICAgICAgICB0aW1lX3N0ZXBzID0gam9iLnRpbWVfcGVyX3N0ZXAoKQogICAgICAgICAgICAgICAgICAgIHJ1bnRpbWUgPSB0aW1lX3N0ZXBzWyJDT01QTEVURUQiXSAtIHRpbWVfc3RlcHNbIlJVTk5JTkciXQogICAgICAgICAgICAgICAgICAgIGV4ZWN1dGlvbl90aW1lID0gam9iLnJlc3VsdCgpLnRpbWVfdGFrZW4KICAgICAgICAgICAgICAgICAgICBwcm92aWRlcl9pbmZvID0geyAKICAgICAgICAgICAgICAgICAgICAgICAgInNob3RzIjogcmVzdWx0LnNob3RzKCksCiAgICAgICAgICAgICAgICAgICAgICAgICJqb2JfaWQiOiBqb2JfaWQsCiAgICAgICAgICAgICAgICAgICAgICAgICJqb2Jfc3RhdHVzIjogc3RyKGpvYi5zdGF0dXMoKSksCiAgICAgICAgICAgICAgICAgICAgICAgICJydW5uaW5nX3N0YXJ0X3RpbWUiOiBzdHIodGltZV9zdGVwc1siUlVOTklORyJdKSwKICAgICAgICAgICAgICAgICAgICAgICAgImNvbXBsZXRpb25fdGltZSI6IHN0cih0aW1lX3N0ZXBzWyJDT01QTEVURUQiXSksCiAgICAgICAgICAgICAgICAgICAgICAgICJ0b3RhbF9ydW5fdGltZSI6IHJ1bnRpbWUudG90YWxfc2Vjb25kcygpLAogICAgICAgICAgICAgICAgICAgICAgICAiZXhlY3V0aW9uX3RpbWUiOiBleGVjdXRpb25fdGltZQogICAgICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICBqc29uX3Jlc3BvbnNlID0gewogICAgICAgICAgICAgICAgICAgICJyZXN1bHQiOiBpbnQobWF4KHJlc3VsdCwga2V5PXJlc3VsdC5nZXQpLDIpLAogICAgICAgICAgICAgICAgICAgICJiYWNrZW5kX2RldmljZSI6IHN0cihiYWNrZW5kKSwKICAgICAgICAgICAgICAgICAgICAiZGV0YWlsIjogewogICAgICAgICAgICAgICAgICAgICAgICAicHJvdmlkZXJfaW5mbyI6IHByb3ZpZGVyX2luZm8sCiAgICAgICAgICAgICAgICAgICAgICAgICJyYW5kb21fbnVtYmVyX2JpbmFyeSI6IG1heChyZXN1bHQsIGtleT1yZXN1bHQuZ2V0KSwKICAgICAgICAgICAgICAgICAgICAgICAgImNvdW50cyI6IG1heChyZXN1bHQudmFsdWVzKCkpLAogICAgICAgICAgICAgICAgICAgICAgICAiYWxsX3Bvc3NpYmxlX3ZhbHVlcyI6IHtrOiBpbnQoaywyKSBmb3Igayx2IGluIHJlc3VsdC5pdGVtcygpIGlmIHYgPT0gbWF4KHJlc3VsdC52YWx1ZXMoKSl9CiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgcmV0dXJuIHsKICAgICAgICAgICAgICAgICAgICAgICAgInN0YXR1c0NvZGUiOiAyMDAsCiAgICAgICAgICAgICAgICAgICAgICAgICJib2R5IjoganNvbl9yZXNwb25zZQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIGpvYiA9IHN1Ym1pdEpvYihjaXJjdWl0LCBiYWNrZW5kLCBzaG90cykKICAgICAgICAgICAgICAgIGpvYi5yZWZyZXNoKCkKICAgICAgICAgICAgICAgIGpzb25fcmVzcG9uc2UgPSB7CiAgICAgICAgICAgICAgICAgICAgImpvYl9pZCI6IHN0cihqb2Iuam9iX2lkKCkpLAogICAgICAgICAgICAgICAgICAgICJodWIiOiBiYWNrZW5kX2luZm8uZ2V0KCJodWIiKSwKICAgICAgICAgICAgICAgICAgICAiYmFja2VuZCI6IHN0cihiYWNrZW5kKSwKICAgICAgICAgICAgICAgICAgICAiam9iX3N1Ym1pdHRlZF90aW1lIjogc3RyKGpvYi5jcmVhdGlvbl9kYXRlKCkpICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgcmV0dXJuIHsKICAgICAgICAgICAgICAgICAgICAgICAgInN0YXR1c0NvZGUiOiAyMDAsCiAgICAgICAgICAgICAgICAgICAgICAgICJib2R5IjoganNvbl9yZXNwb25zZQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICBlbHNlOgogICAgICAgICAgICByZXR1cm4gewogICAgICAgICAgICAgICAgInN0YXR1c0NvZGUiOiA0MDAsCiAgICAgICAgICAgICAgICAiYm9keSI6ICJFcnJvcjogSW52YWxpZCBpbnB1dCBudW1iZXIuIFBsZWFzZSBpbnB1dCB0aGUgbGVuZ3RoIG9mIHJhbmRvbSBudW1iZXIgeW91IHdhbnQgdG8gZ2VuZXJhdGUgKDwgNjUgcXViaXRzKSwgdXNlIHRoZSBmb2xsb3dpbmcgSlNPTiBmb3JtYXQgXG4iICsganNvbi5kdW1wcyhqc29uX2Zvcm1hdCkKICAgICAgICAgICAgfQogICAgZWxzZToKICAgICAgICAgICAgcmV0dXJuIHsKICAgICAgICAgICAgICAgICJzdGF0dXNDb2RlIjogNDAwLAogICAgICAgICAgICAgICAgImJvZHkiOiAiRXJyb3I6IEludmFsaWQgaW5wdXQgZm9ybWF0LiBQbGVhc2UgdXNlIHRoZSBmb2xsb3dpbmcgSlNPTiBmb3JtYXQgZm9yIGlucHV0IGRhdGE6IFxuIiArIGpzb24uZHVtcHMoanNvbl9mb3JtYXQpCiAgICAgICAgICAgIH0=",
                    "handlerQs": "",
                },
                "public": 0,
            }
        }


class ScaleFunctionModel(BaseModel):
    replicas: int = Field(...)

    class Config:
        schema_extra = {"example": {"replicas": 1}}


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
