from pydantic import Field
from typing import List, Literal, Optional
from base_schema import BaseExtractionSchema

# 1. Lock down the exact wording of the Antecedent checkboxes
AntecedentOptions = Literal[
    "Appeared sick or in pain",
    "Preferred item/activity denied",
    "Demand situation",
    "Highly stimulating environment or activity",
    "Attention given to others",
    "No materials or activities",
    "Item(s) removed/activity Terminated"
]

# 2. Lock down the exact wording of the Consequence checkboxes
ConsequenceOptions = Literal[
    "Physical discomfort relieved",
    "Verbal redirection",
    "Interruption/Blocking response",
    "Nothing/ignored",
    "Social attention",
    "Physically guided to comply",
    "Task was removed",
    "Denied access to item/activity",
    "Access to preferred item/activity"
]

class ReportSchema(BaseExtractionSchema):
    # --- CORE FIELDS TO EXTRACT ---
    date_time: str = Field(description="Date and time of the event")
    
    # --- ANTECEDENTS ---
    antecedents: List[AntecedentOptions] = Field(
        default=[],
        description="""
        Select all standard triggers that apply. 
        DEFINITION: An Antecedent (A) is the trigger occurring immediately before the behavior.
        
        MAPPING GLOSSARY:
        - "Appeared sick or in pain": Use if the teacher notes the child seemed unwell, was holding their stomach/head, had an injury, or showed signs of physical distress.
        - "Preferred item/activity denied": Use if the child asked for something they wanted (like a toy, iPad, or recess) and was told "no" or told they had to wait.
        - "Demand situation": Use if the teacher gave an instruction, asked the child to do schoolwork, placed a rule/demand, or forced a transition to a new activity.
        - "Highly stimulating environment or activity": Use for loud noises (fire alarms, assemblies), bright lights, chaotic/crowded rooms, or overwhelming sensory inputs.
        - "Attention given to others": Use if the teacher or caregiver was talking to, praising, or helping another student when the behavior started.
        - "No materials or activities": Use if the child was waiting, had nothing to do, or lacked access to engaging materials (unstructured downtime/boredom).
        - "Item(s) removed/activity Terminated": Use if an item the child was *already* actively using was taken out of their hands, or an activity they were actively playing was ended.
        """
    )
    other_antecedent_text: Optional[str] = Field(
        default=None,
        description="If the antecedent does not fit any standard options, describe it briefly here."
    )
    
    # --- BEHAVIOUR ---
    behaviour: str = Field(
        description="DEFINITION - Behavior (B): The observable action or response of the individual (e.g., yelling, smiling, following instructions). Provide a detailed, narrative description of what exactly the child did."
    )
    
    # --- CONSEQUENCES ---
    consequences: List[ConsequenceOptions] = Field(
        default=[],
        description="""
        Select all standard responses applied by the caregiver. 
        DEFINITION: A Consequence (C) is the immediate result or teacher response following the behavior.
        
        MAPPING GLOSSARY:
        - "Physical discomfort relieved": Use if the teacher gave medicine, an ice pack, a band-aid, a snack/water, or changed the environment to relieve physical pain.
        - "Verbal redirection": Use if the teacher talked to the student to calm them down, reminded them of the rules, prompted a different behavior, or offered a verbal choice.
        - "Interruption/Blocking response": Use if the teacher had to physically step in between the child and an object/person for safety, blocked a hit, or stopped them from running away.
        - "Nothing/ignored": Use if the teacher used 'planned ignoring', intentionally gave no attention to the behavior, or just stood back and waited it out.
        - "Social attention": Use if the teacher gave hugs, physical comfort, eye contact, or engaged in deep conversation directly as a result of the behavior.
        - "Physically guided to comply": Use if the teacher used hand-over-hand assistance or gently physically moved the child's body to help them complete the original task.
        - "Task was removed": Use if the teacher gave up on the demand, allowed the child to stop working, or took the assignment away completely.
        - "Denied access to item/activity": Use if the consequence of the behavior was losing a privilege, going to time-out, or being firmly told they cannot have the item.
        - "Access to preferred item/activity": Use if the child was eventually given the toy, iPad, or activity they wanted, or if they were given a sensory tool (like a chewy or weighted blanket) to calm down.
        """
    )
    other_consequence_text: Optional[str] = Field(
        default=None,
        description="If the consequence does not fit any standard options, describe it briefly here."
    )

    # --- PDF MAPPING CONFIGURATION ---
    class LayoutConfig:
        layout_type = "UNIQUE"
        
        # Map our text/string fields to the exact Names of the text boxes in the PDF
        text_mapping = {
            "date_time": "date_time_box",
            "behaviour": "behaviour_box",
            "other_antecedent_text": "other_antecedent_line",
            "other_consequence_text": "other_consequence_line"
        }
        
        # Map the Pydantic options to the exact Names of checkboxes in the PDF
        checkbox_mapping = {
            "antecedents": {
                "Appeared sick or in pain": "chk_ant_sick",
                "Preferred item/activity denied": "chk_ant_denied",
                "Demand situation": "chk_ant_demand",
                "Highly stimulating environment or activity": "chk_ant_stimulating",
                "Attention given to others": "chk_ant_attention",
                "No materials or activities": "chk_ant_no_materials",
                "Item(s) removed/activity Terminated": "chk_ant_terminated"
            },
            "consequences": {
                "Physical discomfort relieved": "chk_con_relieved",
                "Verbal redirection": "chk_con_verbal",
                "Interruption/Blocking response": "chk_con_blocking",
                "Nothing/ignored": "chk_con_ignored",
                "Social attention": "chk_con_social",
                "Physically guided to comply": "chk_con_guided",
                "Task was removed": "chk_con_task_removed",
                "Denied access to item/activity": "chk_con_denied_item",
                "Access to preferred item/activity": "chk_con_access_item"
            }
        }
        
        # (Optional but recommended) If these text fields have data, 
        # tell your main.py to automatically check these corresponding "Other" boxes
        other_antecedent_checkbox = "chk_ant_other"
        other_consequence_checkbox = "chk_con_other"