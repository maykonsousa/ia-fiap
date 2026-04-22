-- Script de provisionamento do banco.
-- Executado automaticamente pela imagem Oracle Database Free
-- na PRIMEIRA criacao do container (via /opt/oracle/scripts/setup/).
-- Cria um usuario dedicado "fiap" dentro da PDB FREEPDB1.

ALTER SESSION SET CONTAINER = FREEPDB1;

CREATE USER fiap IDENTIFIED BY fiap123;

GRANT CONNECT, RESOURCE, CREATE SESSION TO fiap;
GRANT UNLIMITED TABLESPACE TO fiap;

EXIT;
