from pydantic import BaseModel, Field


class CareerAdvice(BaseModel):
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)
    recommended_certifications: list[str] = Field(default_factory=list)
    learning_resources: list[str] = Field(default_factory=list)

class CareerAdviceResponse(BaseModel):
    advice: CareerAdvice
    sources: list[str] = Field(default_factory=list)    
    