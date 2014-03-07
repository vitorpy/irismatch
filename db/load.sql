-- creates tables on the workflow namespace

create table if not exists Workflow.Items(ItemId integer primary key, State integer);

create table if not exists Workflow.Attributes(ItemId integer, Name varchar(100), StrValue varchar(100));

create table if not exists Workflow.ActivitiesStates(State integer primary key, Descriptiom varchar(100));

-- fill the default values

--insert into Workflow.ActivitiesStates
-- finish....


