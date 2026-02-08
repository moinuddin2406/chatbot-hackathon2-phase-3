from typing import Dict, Any, List, Optional
from ..schemas.chat_schemas import ToolCall, ToolCallResult
import random


class MockCohereClient:
    def __init__(self):
        # Simulate a working client without requiring an API key
        pass

    def _detect_urdu(self, message: str) -> bool:
        """
        Detect if the message contains Urdu text by checking for common Urdu words/characters
        """
        urdu_words = [
            "task", "ka", "ko", "hai", "karna", "kar", "do", "karo", 
            "ye", "yeh", "hain", "naam", "description", "title",
            "aur", "par", "se", "ne", "hi", "ji", "jiye", "kya"
        ]
        
        # Check for Urdu characters (Arabic script used for Urdu)
        urdu_chars = set(range(0x600, 0x6FF + 1))  # Arabic/Persian-Arabic characters
        
        for char in message:
            if ord(char) in urdu_chars:
                return True
        
        # Check for common Urdu words
        words = message.lower().split()
        for word in words:
            if word in urdu_words:
                return True
        
        return False

    def _should_add_task(self, message_lower: str) -> bool:
        """
        Determine if the message is requesting to add a task
        """
        return (("add task" in message_lower or "create task" in message_lower or "new task" in message_lower) and 
                not any(word in message_lower for word in ["update task", "edit task", "change task", "karo task", "kar do"])) or \
               ("add" in message_lower and "task" in message_lower and 
                not any(word in message_lower for word in ["update task", "edit task", "change task", "karo", "kar do"])) or \
               ("create" in message_lower and "task" in message_lower and 
                not any(word in message_lower for word in ["update task", "edit task", "change task", "karo", "kar do"])) or \
               "add a task" in message_lower or \
               "task add karo" in message_lower or \
               "task add kar do" in message_lower

    def _should_update_task(self, message_lower: str) -> bool:
        """
        Determine if the message is requesting to update a task
        """
        # Check for specific update-related terms
        update_indicators = ["update task", "edit task", "change task", "task update", "task edit", "task change"]
        for indicator in update_indicators:
            if indicator in message_lower:
                return True
        
        # Check for specific update patterns with task IDs
        update_patterns = ["task ko update", "task ko edit", "task ko change", "task ka naam change"]
        for pattern in update_patterns:
            if pattern in message_lower:
                return True
        
        # Check for specific update with karo/kar do
        specific_update_patterns = ["task ko update karo", "task ko update kar do"]
        for pattern in specific_update_patterns:
            if pattern in message_lower:
                return True
        
        # Check for flexible patterns like "task [id] ko update karo"
        import re
        if re.search(r'task\s+\d+\s+ko\s+update\s+karo', message_lower) or \
           re.search(r'task\s+\d+\s+ko\s+update\s+kar\s+do', message_lower) or \
           re.search(r'task\s+\d+\s+ko\s+edit\s+karo', message_lower) or \
           re.search(r'task\s+\d+\s+ko\s+change\s+karo', message_lower):
            return True
        
        # Check for general update with karo/kar do
        if ("update" in message_lower or "edit" in message_lower or "change" in message_lower) and \
           ("karo" in message_lower or "kar do" in message_lower):
            return True
        
        return False

    def _should_list_tasks(self, message_lower: str) -> bool:
        """
        Determine if the message is requesting to list tasks
        """
        # Check for English phrases
        english_phrases = ["list tasks", "my tasks", "show tasks", "task list", "tasks list", "all tasks"]
        # Check for Urdu/Hindi phrases
        urdu_phrases = ["tasks dekho", "mera tasks", "sab tasks", "task dikhao", "sare tasks", "tasks dikhao"]
        
        return any(phrase in message_lower for phrase in english_phrases + urdu_phrases)

    def _should_complete_task(self, message_lower: str) -> bool:
        """
        Determine if the message is requesting to complete a task
        """
        # Check for specific complete-related terms
        complete_indicators = ["complete task", "finish task", "done task", "mark as done", "task complete", "task finish", "task done"]
        for indicator in complete_indicators:
            if indicator in message_lower:
                return True
        
        # Check for specific complete patterns with task IDs
        complete_patterns = ["task ko complete", "task ko finish", "task ko done", "ho gaya", "hogaya", "khatam"]
        for pattern in complete_patterns:
            if pattern in message_lower:
                return True
        
        # Check for specific complete with karo/kar do
        specific_complete_patterns = ["is task ko complete karo", "task ko complete karo", "task ko complete kar do"]
        for pattern in specific_complete_patterns:
            if pattern in message_lower:
                return True
        
        # Check for flexible patterns like "task [id] ko complete karo"
        import re
        if re.search(r'task\s+\d+\s+ko\s+complete\s+karo', message_lower) or \
           re.search(r'task\s+\d+\s+ko\s+complete\s+kar\s+do', message_lower) or \
           re.search(r'task\s+\d+\s+ko\s+finish\s+karo', message_lower) or \
           re.search(r'task\s+\d+\s+ko\s+done\s+karo', message_lower):
            return True
        
        # Check for mark task as done pattern
        if "mark task" in message_lower and "done" in message_lower:
            return True
        
        # Check for general complete with karo/kar do
        if ("complete" in message_lower or "finish" in message_lower or "done" in message_lower) and \
           ("karo" in message_lower or "kar do" in message_lower):
            return True
        
        return False

    def _should_delete_task(self, message_lower: str) -> bool:
        """
        Determine if the message is requesting to delete a task
        """
        # Check for specific delete-related terms
        delete_indicators = ["delete task", "remove task", "task delete", "task remove"]
        for indicator in delete_indicators:
            if indicator in message_lower:
                return True
        
        # Check for specific delete patterns with task IDs
        delete_patterns = ["task ko delete", "task ko nikal", "task ko hata"]
        for pattern in delete_patterns:
            if pattern in message_lower:
                return True
        
        # Check for specific delete with kar do
        specific_delete_patterns = ["yeh task delete kar do"]
        for pattern in specific_delete_patterns:
            if pattern in message_lower:
                return True
        
        # Check for flexible patterns like "task [id] nikal do" or "yeh task [id] delete kar do"
        import re
        if re.search(r'yeh\s+task\s+\d+\s+delete\s+kar\s+do', message_lower) or \
           re.search(r'task\s+\d+\s+nikal\s+do', message_lower) or \
           re.search(r'task\s+\d+\s+hata\s+do', message_lower) or \
           re.search(r'task\s+\d+\s+delete\s+kar\s+do', message_lower):
            return True
        
        # Check for general delete with kar do
        if ("delete" in message_lower or "remove" in message_lower or "nikal" in message_lower or "hata" in message_lower) and \
           ("kar do" in message_lower or "do" in message_lower):
            return True
        
        return False

    def chat_with_tools(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Mock implementation that simulates Cohere responses with multilingual support
        """
        # Detect language and normalize message
        message_lower = message.lower()
        
        tool_calls = []

        # Detect if the user wants to add a task
        if self._should_add_task(message_lower):
            # Extract title and description using more sophisticated parsing
            title = "New Task"
            description = ""
            due_date = None

            # First, try to extract title and description using specific patterns
            import re

            # Look for title pattern: "title is [value]" or "is task ka title [value]"
            title_match = re.search(r"(?:title is|is task ka title|ka naam)\s+([^andaur.]+?)(?:\s+(?:and|aur|par|$|description|due date))", message, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()

            # Look for description pattern: "description is [value]" or "is task ka description [value]"
            desc_match = re.search(r"(?:description is|is task ka description|ye hai)\s+([^andaur.]+?)(?:\s+(?:and|aur|par|$|due date))", message, re.IGNORECASE)
            if desc_match:
                description = desc_match.group(1).strip()

            # Look for due date pattern: "due date is [value]" or "due date [value]" or "by [date]"
            due_date_match = re.search(r"(?:due date is|due date|by|till|before)\s+([^andaur.]+?)(?:\s+(?:and|aur|par|$))", message, re.IGNORECASE)
            if due_date_match:
                due_date_candidate = due_date_match.group(1).strip()
                
                # Try to parse the due date in various formats
                import datetime
                # Common date formats to try
                date_formats = [
                    "%Y-%m-%d",  # YYYY-MM-DD
                    "%m/%d/%Y",  # MM/DD/YYYY
                    "%d/%m/%Y",  # DD/MM/YYYY
                    "%m-%d-%Y",  # MM-DD-YYYY
                    "%d-%m-%Y",  # DD-MM-YYYY
                    "%B %d, %Y", # Month DD, YYYY
                    "%d %B %Y",  # DD Month YYYY
                    "%m/%d",     # MM/DD (current year)
                    "%d/%m",     # DD/MM (current year)
                ]
                
                for fmt in date_formats:
                    try:
                        if fmt in ["%m/%d", "%d/%m"]:  # Date without year, assume current year
                            parsed_date = datetime.datetime.strptime(due_date_candidate + f"/{datetime.datetime.now().year}", fmt)
                        else:
                            parsed_date = datetime.datetime.strptime(due_date_candidate, fmt)
                        
                        due_date = parsed_date.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
                
                # If still no valid date, check for relative dates
                if not due_date:
                    due_date_lower = due_date_candidate.lower()
                    today = datetime.date.today()
                    
                    if "today" in due_date_lower:
                        due_date = today.strftime("%Y-%m-%d")
                    elif "tomorrow" in due_date_lower:
                        due_date = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    elif "day after tomorrow" in due_date_lower or "kal kal" in due_date_lower:
                        due_date = (today + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
                    elif "this week" in due_date_lower:
                        # Set to end of current week (Sunday)
                        days_until_sunday = 6 - today.weekday()  # Monday is 0, Sunday is 6
                        due_date = (today + datetime.timedelta(days=days_until_sunday)).strftime("%Y-%m-%d")
                    elif "next week" in due_date_lower:
                        # Set to same day next week
                        due_date = (today + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
                    elif "this weekend" in due_date_lower:
                        # Set to next Saturday
                        days_until_saturday = 5 - today.weekday()
                        if days_until_saturday <= 0:  # If it's already past Saturday
                            days_until_saturday += 7
                        due_date = (today + datetime.timedelta(days=days_until_saturday)).strftime("%Y-%m-%d")

            # If no specific title/description found, try to extract from simpler patterns
            if title == "New Task":
                # Look for patterns like "add task [title]" or "create task [title]"
                add_task_match = re.search(r"(?:add task|create task|new task|add a task)\s+(.+?)(?:$|description is|title is|due date is)", message, re.IGNORECASE)
                if add_task_match:
                    extracted = add_task_match.group(1).strip()
                    # Clean up the extracted title
                    if extracted and not extracted.startswith("description is") and not extracted.startswith("title is") and not extracted.startswith("due date"):
                        title = extracted

            # If still no title, try to extract from the main message
            if title == "New Task":
                # For simple cases like "add task Buy groceries", "create task Call dentist", etc.
                # More comprehensive pattern to catch various formats
                simple_match = re.search(r"(?:add\s+task|create\s+task|new\s+task|add\s+a\s+task)\s+(.+?)(?:\s+(?:due date|by|till|before)|$)", message, re.IGNORECASE)
                if simple_match:
                    title = simple_match.group(1).strip()
                    # Further clean up by removing common trailing phrases
                    if " and " in title:
                        # Split on 'and' if it's not part of the actual title
                        parts = title.split(" and ", 1)
                        title = parts[0].strip()

            # Prepare parameters for the tool call
            params = {
                "title": title or "New Task",
                "description": description or None
            }
            
            # Add due_date to parameters if it was found
            if due_date:
                params["due_date"] = due_date

            tool_calls.append({
                "name": "add_task",
                "parameters": params
            })
        # Detect if the user wants to update a task (comes after add task to avoid conflicts)
        elif self._should_update_task(message_lower):
            # Extract task ID and details using more sophisticated parsing
            import re

            # Look for task ID in the message (numbers after "task" or near update/edit/change words)
            task_id = None
            # First, try to find pattern like "task [number]" after update/edit/change
            update_pos = max(
                message_lower.find("update"),
                message_lower.find("edit"),
                message_lower.find("change"),
                message_lower.find("karo"),  # Urdu "do"
                message_lower.find("kar do")
            )
            if update_pos != -1:
                # Look for the next number after the update position
                remaining_msg = message[update_pos:]
                # Match patterns like "task 123" or "123 task"
                task_id_matches = re.findall(r'task\s+(\d+)|(\d+)\s+task', remaining_msg, re.IGNORECASE)
                if task_id_matches:
                    # Extract the first number found
                    for match in task_id_matches:
                        task_id = match[0] or match[1]  # Take first non-empty group
                        if task_id:
                            break

            # If still no task ID found, look for any number in the message
            if not task_id:
                task_id_matches = re.findall(r'\d+', message)
                task_id = task_id_matches[0] if task_id_matches else None

            # Extract title, description and due date if mentioned
            title = None
            description = None
            due_date = None

            # Look for title pattern: "title is [value]", "ka naam [value]", or "[value] karna"
            title_match = re.search(r'(?:title is|ka naam|karna)\s+([^andaur.]+?)(?:\s+(?:and|aur|par|$|due date))', message, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()

            # Look for description pattern: "description is [value]", "ka description [value]", "ye [value]"
            desc_match = re.search(r'(?:description is|ka description|ye hai)\s+([^andaur.]+?)(?:\s+(?:and|aur|par|$|due date))', message, re.IGNORECASE)
            if desc_match:
                description = desc_match.group(1).strip()

            # Look for due date pattern: "due date is [value]" or "due date [value]" or "by [date]"
            due_date_match = re.search(r'(?:due date is|due date|by|till|before)\s+([^andaur.]+?)(?:\s+(?:and|aur|par|$))', message, re.IGNORECASE)
            if due_date_match:
                due_date_candidate = due_date_match.group(1).strip()
                
                # Try to parse the due date in various formats
                import datetime
                # Common date formats to try
                date_formats = [
                    "%Y-%m-%d",  # YYYY-MM-DD
                    "%m/%d/%Y",  # MM/DD/YYYY
                    "%d/%m/%Y",  # DD/MM/YYYY
                    "%m-%d-%Y",  # MM-DD-YYYY
                    "%d-%m-%Y",  # DD-MM-YYYY
                    "%B %d, %Y", # Month DD, YYYY
                    "%d %B %Y",  # DD Month YYYY
                    "%m/%d",     # MM/DD (current year)
                    "%d/%m",     # DD/MM (current year)
                ]
                
                for fmt in date_formats:
                    try:
                        if fmt in ["%m/%d", "%d/%m"]:  # Date without year, assume current year
                            parsed_date = datetime.datetime.strptime(due_date_candidate + f"/{datetime.datetime.now().year}", fmt)
                        else:
                            parsed_date = datetime.datetime.strptime(due_date_candidate, fmt)
                        
                        due_date = parsed_date.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
                
                # If still no valid date, check for relative dates
                if not due_date:
                    due_date_lower = due_date_candidate.lower()
                    today = datetime.date.today()
                    
                    if "today" in due_date_lower:
                        due_date = today.strftime("%Y-%m-%d")
                    elif "tomorrow" in due_date_lower:
                        due_date = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    elif "day after tomorrow" in due_date_lower or "kal kal" in due_date_lower:
                        due_date = (today + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
                    elif "this week" in due_date_lower:
                        # Set to end of current week (Sunday)
                        days_until_sunday = 6 - today.weekday()  # Monday is 0, Sunday is 6
                        due_date = (today + datetime.timedelta(days=days_until_sunday)).strftime("%Y-%m-%d")
                    elif "next week" in due_date_lower:
                        # Set to same day next week
                        due_date = (today + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
                    elif "this weekend" in due_date_lower:
                        # Set to next Saturday
                        days_until_saturday = 5 - today.weekday()
                        if days_until_saturday <= 0:  # If it's already past Saturday
                            days_until_saturday += 7
                        due_date = (today + datetime.timedelta(days=days_until_saturday)).strftime("%Y-%m-%d")

            # If no specific title/description/due_date provided, extract meaningful content
            if not title and not description and not due_date:
                # Extract content after the task ID
                if task_id:
                    # Find the position of the task ID in the message
                    task_pos = re.search(rf'\b{task_id}\b', message, re.IGNORECASE)
                    if task_pos:
                        after_task = message[task_pos.end():].strip()
                        if after_task:
                            # Look for patterns like "with title [value]" or "ka naam [value]"
                            title_match = re.search(r'(?:with|and|ka naam|karna)\s+(.+?)(?:\s+(?:and|aur|par|$|due date))', after_task, re.IGNORECASE)
                            if title_match:
                                title = title_match.group(1).strip()

                            desc_match = re.search(r'(?:with|and|ka description|ye|yeh)\s+(.+?)(?:\s+(?:and|aur|par|$|due date))', after_task, re.IGNORECASE)
                            if desc_match:
                                description = desc_match.group(1).strip()

            # Additional logic to extract title/description/due_date from common update patterns
            if not title and not description and not due_date:
                # Pattern: "update task 123 title is new title and description is new description"
                # More flexible pattern to match various update formats
                update_match = re.search(rf'(?:update|edit|change)\s+task\s+{task_id}.*?(?:title is|ka naam)\s+(.+?)(?:\s+(?:and|aur|description is|ka description|due date is)\s+(.+?)(?:\s+(?:and|aur|due date is)\s+(.+?)(?:\s+(?:and|aur)|$)|\s+(?:and|aur)|$)|\s+(?:and|aur)|$)', message, re.IGNORECASE)
                if update_match:
                    title = update_match.group(1).strip()
                    if update_match.lastindex >= 2 and update_match.group(2):
                        description = update_match.group(2).strip()
                    if update_match.lastindex >= 3 and update_match.group(3):
                        due_date_candidate = update_match.group(3).strip()
                        # Parse the due date similarly as above
                        for fmt in date_formats:
                            try:
                                if fmt in ["%m/%d", "%d/%m"]:  # Date without year, assume current year
                                    parsed_date = datetime.datetime.strptime(due_date_candidate + f"/{datetime.datetime.now().year}", fmt)
                                else:
                                    parsed_date = datetime.datetime.strptime(due_date_candidate, fmt)
                                
                                due_date = parsed_date.strftime("%Y-%m-%d")
                                break
                            except ValueError:
                                continue
                        
                        # If still no valid date, check for relative dates
                        if not due_date:
                            due_date_lower = due_date_candidate.lower()
                            today = datetime.date.today()
                            
                            if "today" in due_date_lower:
                                due_date = today.strftime("%Y-%m-%d")
                            elif "tomorrow" in due_date_lower:
                                due_date = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                            elif "day after tomorrow" in due_date_lower or "kal kal" in due_date_lower:
                                due_date = (today + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
                            elif "this week" in due_date_lower:
                                # Set to end of current week (Sunday)
                                days_until_sunday = 6 - today.weekday()  # Monday is 0, Sunday is 6
                                due_date = (today + datetime.timedelta(days=days_until_sunday)).strftime("%Y-%m-%d")
                            elif "next week" in due_date_lower:
                                # Set to same day next week
                                due_date = (today + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
                            elif "this weekend" in due_date_lower:
                                # Set to next Saturday
                                days_until_saturday = 5 - today.weekday()
                                if days_until_saturday <= 0:  # If it's already past Saturday
                                    days_until_saturday += 7
                                due_date = (today + datetime.timedelta(days=days_until_saturday)).strftime("%Y-%m-%d")

            if task_id:
                params = {"task_id": task_id}
                if title:
                    params["title"] = title
                if description:
                    params["description"] = description
                if due_date:
                    params["due_date"] = due_date

                tool_calls.append({
                    "name": "update_task",
                    "parameters": params
                })
        # Detect if the user wants to list tasks
        elif self._should_list_tasks(message_lower):
            # Determine the status filter from the message
            status = "all"  # Default to all
            if "completed" in message_lower:
                status = "completed"
            elif "pending" in message_lower or "incomplete" in message_lower:
                status = "pending"
            
            tool_calls.append({
                "name": "list_tasks",
                "parameters": {
                    "status": status
                }
            })
        # Detect if the user wants to complete a task
        elif self._should_complete_task(message_lower):
            # Extract task ID if mentioned using more sophisticated parsing
            import re
            
            # Look for task ID in the message (numbers after "task" or near complete/finish/done words)
            task_id = None
            # First, try to find pattern like "task [number]" after complete/finish/done
            for word in ["complete", "finish", "done", "ho gaya", "hogaya", "khatam"]:
                pos = message_lower.find(word)
                if pos != -1:
                    # Look for the next number after the complete/finish/done position
                    remaining_msg = message[pos:]
                    task_id_matches = re.findall(r'task\s+(\d+)|(\d+)\s+task', remaining_msg, re.IGNORECASE)
                    if task_id_matches:
                        for match in task_id_matches:
                            task_id = match[0] or match[1]  # Take first non-empty group
                            if task_id:
                                break
                        break
            
            # If still no task ID found, look for any number in the message
            if not task_id:
                task_id_matches = re.findall(r'\d+', message)
                task_id = task_id_matches[0] if task_id_matches else None
            
            # If still no task ID, default to "1"
            if not task_id:
                task_id = "1"

            tool_calls.append({
                "name": "complete_task",
                "parameters": {
                    "task_id": task_id
                }
            })
        # Detect if the user wants to delete a task
        elif self._should_delete_task(message_lower):
            # Extract task ID if mentioned using more sophisticated parsing
            import re
            
            # Look for task ID in the message (numbers after "task" or near delete/remove words)
            task_id = None
            # First, try to find pattern like "task [number]" after delete/remove
            for word in ["delete", "remove", "nikal", "hata", "delete"]:
                pos = message_lower.find(word)
                if pos != -1:
                    # Look for the next number after the delete/remove position
                    remaining_msg = message[pos:]
                    task_id_matches = re.findall(r'task\s+(\d+)|(\d+)\s+task', remaining_msg, re.IGNORECASE)
                    if task_id_matches:
                        for match in task_id_matches:
                            task_id = match[0] or match[1]  # Take first non-empty group
                            if task_id:
                                break
                        break
            
            # If still no task ID found, look for any number in the message
            if not task_id:
                task_id_matches = re.findall(r'\d+', message)
                task_id = task_id_matches[0] if task_id_matches else None
            
            # If still no task ID, default to "1"
            if not task_id:
                task_id = "1"

            tool_calls.append({
                "name": "delete_task",
                "parameters": {
                    "task_id": task_id
                }
            })

        # Generate a simple response based on the message
        responses = [
            f"I understood your message: '{message}'. How else can I assist you?",
            f"Thanks for your input: '{message}'. What else would you like to do?",
            f"I've processed your request: '{message}'. Is there anything else I can help with?",
            f"Your message '{message}' has been noted. How can I further assist you?"
        ]
        
        # Use Urdu response if the message contains Urdu
        if self._detect_urdu(message_lower):
            responses = [
                f"میں آپ کی درخواست سمجھ گیا: '{message}'. کیا آپ کی کوئی اور مدد چاہیے؟",
                f"آپ کا پیغام سمجھا: '{message}'. اور کچھ کر سکتا ہوں میں؟",
                f"میں نے آپ کی درخواست پر عمل کیا: '{message}'. کیسے اور مدد کر سکتا ہوں؟",
                f"آپ کی درخواست نوٹ کر لی: '{message}'. اور کچھ چاہیے کیا؟"
            ]

        import random
        response_text = random.choice(responses)

        return {
            "text": response_text,
            "tool_calls": tool_calls
        }

    def process_tool_results(
        self,
        original_message: str,
        conversation_history: List[Dict[str, str]],
        tool_results: List[Dict[str, Any]]
    ) -> str:
        """
        Process the results from tool executions and generate a final response
        """
        # Generate a response acknowledging the tool results
        if tool_results:
            success_count = sum(1 for result in tool_results if result['result'].get('success', False))
            total_count = len(tool_results)

            if success_count == total_count:
                return f"I've successfully completed {success_count} task(s) for you. How else can I assist?"
            else:
                return f"I processed your request with {success_count} out of {total_count} tasks completed successfully. How else can I help?"
        else:
            return "I've processed your request. How else can I assist you?"


# Global instance of the mock Cohere client
mock_cohere_client = MockCohereClient()