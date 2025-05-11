CREATE TABLE SETTINGS
(
    key   text not null,
    value text not null
);

CREATE TABLE RECENT_FILES
(
    path          text not null,
    date_accessed text not null
);