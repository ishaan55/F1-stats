from fastapi.responses import JSONResponse
import uvicorn
from setup import app
from utils import extract_gp_info, analysis

@app.get("/api/race-summary")
def get_event(gp: str):
    try:
        gp_info = extract_gp_info(gp)
        if not gp_info:
            return JSONResponse(status_code=404, content={"message": "Grand Prix not found"})
        year = gp_info["year"]
        event = gp_info["event"]

        analysis_result = analysis(year, event)
        if not analysis_result:
            return JSONResponse(status_code=404, content={"message": "Analysis not found"})
        return analysis_result
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)