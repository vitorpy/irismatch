Brief description:

-- Workflow namespace

* Workflow.Items
 |-> ItemId, Activity, State (FK)

* Workflow.Attributes
 |-> ItemId (FK), Name, Value

* Workflow.ActivityStates
 |-> State, Description (Queued, Running, Waiting, Completed, Rejected)

-- IrisMatch namespace

* IrisMatch.IrisID
 |-> IrisID, Template (BLOB), State (FK)

* IrisMatch.IrisIDStates
 -> State, Description (Active, Archived, MarkedForDeletion)

