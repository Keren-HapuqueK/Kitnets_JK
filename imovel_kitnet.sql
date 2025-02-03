CREATE TABLE Estado_Civil (
    ID_Estado_Civil SERIAL PRIMARY KEY,
    Desc_Estado_Civil VARCHAR(50)
);

CREATE TABLE Forma_Pagamento (
    ID_Forma_Pagamento SERIAL PRIMARY KEY,
    Desc_Forma_Pgto VARCHAR(50)
);

CREATE TABLE Locador (
    ID_Locador SERIAL PRIMARY KEY,
    Login VARCHAR(50),
    Senha VARCHAR(20),
    Nome VARCHAR(100),
    RG VARCHAR(20),
    CPF_CNPJ VARCHAR(14),
    Telefone VARCHAR(20),
    ID_Estado_Civil INTEGER,
    FOREIGN KEY(ID_Estado_Civil) REFERENCES Estado_Civil (ID_Estado_Civil)
);

CREATE TABLE Locatario (
    ID_Locatario SERIAL PRIMARY KEY,
    Nome VARCHAR(100),
    Telefone VARCHAR(20),
    RG VARCHAR(20),
    CPF_CNPJ VARCHAR(14),
    ID_Estado_Civil INTEGER,
    FOREIGN KEY(ID_Estado_Civil) REFERENCES Estado_Civil (ID_Estado_Civil)
);

CREATE TABLE Imovel (
    ID_Imovel SERIAL PRIMARY KEY,
    Endereco VARCHAR(200),
    Descricao VARCHAR(200),
    Disponivel CHAR(1),
    Vlr_Aluguel NUMERIC(6,2),
    UC INTEGER,
    ID_Locador INTEGER,
    FOREIGN KEY(ID_Locador) REFERENCES Locador (ID_Locador)
);

CREATE TABLE Contrato (
    ID_Contrato SERIAL PRIMARY KEY,
    NU_Contrato INTEGER,
    VLR_Aluguel NUMERIC(6,2),
    DT_Inicio DATE,
    Dia_Base VARCHAR(2),
    DT_Fim DATE,
    Cidade VARCHAR(20),
    UF CHAR(2),
    ID_Imovel INTEGER,
    ID_Locatario INTEGER,
    ID_Locador INTEGER,
    FOREIGN KEY(ID_Imovel) REFERENCES Imovel (ID_Imovel),
    FOREIGN KEY(ID_Locatario) REFERENCES Locatario (ID_Locatario),
    FOREIGN KEY(ID_Locador) REFERENCES Locador (ID_Locador)
);

CREATE TABLE Registro_Pagamento (
    ID_Pagamento SERIAL PRIMARY KEY,
    DT_Paga DATE,
    Ref_Mes_Ano VARCHAR(100),
    Observacao VARCHAR(100),
    ID_Contrato INTEGER,
    ID_Locatario INTEGER,
    ID_Forma_Pagamento INTEGER,
    FOREIGN KEY(ID_Contrato) REFERENCES Contrato (ID_Contrato),
    FOREIGN KEY(ID_Locatario) REFERENCES Locatario (ID_Locatario),
    FOREIGN KEY(ID_Forma_Pagamento) REFERENCES Forma_Pagamento (ID_Forma_Pagamento)
);




CREATE OR REPLACE FUNCTION criar_imovel(
    p_id_locador INTEGER,
    p_endereco VARCHAR,
    p_descricao VARCHAR,
    p_disponivel CHAR,
    p_vlr_aluguel NUMERIC,
    p_uc INTEGER
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Imovel (ID_Locador, Endereco, Descricao, Disponivel, Vlr_Aluguel, UC)
    VALUES (p_id_locador, p_endereco, p_descricao, p_disponivel, p_vlr_aluguel, p_uc);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION editar_imovel(
    p_id_imovel INTEGER,
    p_id_locador INTEGER,
    p_endereco VARCHAR,
    p_descricao VARCHAR,
    p_disponivel CHAR,
    p_vlr_aluguel NUMERIC,
    p_uc INTEGER
) RETURNS VOID AS $$
BEGIN
    UPDATE Imovel
    SET ID_Locador = p_id_locador, Endereco = p_endereco, Descricao = p_descricao, Disponivel = p_disponivel, Vlr_Aluguel = p_vlr_aluguel, UC = p_uc
    WHERE ID_Imovel = p_id_imovel;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION excluir_imovel(
    p_id_imovel INTEGER
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Imovel WHERE ID_Imovel = p_id_imovel;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION criar_contrato(
    p_nu_contrato INTEGER,
    p_vlr_aluguel NUMERIC,
    p_dt_inicio DATE,
    p_dia_base VARCHAR,
    p_dt_fim DATE,
    p_cidade VARCHAR,
    p_uf CHAR,
    p_id_imovel INTEGER,
    p_id_locatario INTEGER,
    p_id_locador INTEGER
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Contrato (NU_Contrato, VLR_Aluguel, DT_Inicio, Dia_Base, DT_Fim, Cidade, UF, ID_Imovel, ID_Locatario, ID_Locador)
    VALUES (p_nu_contrato, p_vlr_aluguel, p_dt_inicio, p_dia_base, p_dt_fim, p_cidade, p_uf, p_id_imovel, p_id_locatario, p_id_locador);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION editar_contrato(
    p_id_contrato INTEGER,
    p_nu_contrato INTEGER,
    p_vlr_aluguel NUMERIC,
    p_dt_inicio DATE,
    p_dia_base VARCHAR,
    p_dt_fim DATE,
    p_cidade VARCHAR,
    p_uf CHAR,
    p_id_imovel INTEGER,
    p_id_locatario INTEGER,
    p_id_locador INTEGER
) RETURNS VOID AS $$
BEGIN
    UPDATE Contrato
    SET NU_Contrato = p_nu_contrato, VLR_Aluguel = p_vlr_aluguel, DT_Inicio = p_dt_inicio, Dia_Base = p_dia_base, DT_Fim = p_dt_fim, Cidade = p_cidade, UF = p_uf, ID_Imovel = p_id_imovel, ID_Locatario = p_id_locatario, ID_Locador = p_id_locador
    WHERE ID_Contrato = p_id_contrato;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION excluir_contrato(
    p_id_contrato INTEGER
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Contrato WHERE ID_Contrato = p_id_contrato;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION criar_locador(
    p_nome VARCHAR,
    p_telefone VARCHAR,
    p_rg VARCHAR,
    p_cpf_cnpj VARCHAR,
    p_id_estado_civil INTEGER
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Locador (Nome, Telefone, RG, CPF_CNPJ, ID_Estado_Civil)
    VALUES (p_nome, p_telefone, p_rg, p_cpf_cnpj, p_id_estado_civil);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION editar_locador(
    p_id_locador INTEGER,
    p_nome VARCHAR,
    p_telefone VARCHAR,
    p_rg VARCHAR,
    p_cpf_cnpj VARCHAR,
    p_id_estado_civil INTEGER
) RETURNS VOID AS $$
BEGIN
    UPDATE Locador
    SET Nome = p_nome, Telefone = p_telefone, RG = p_rg, CPF_CNPJ = p_cpf_cnpj, ID_Estado_Civil = p_id_estado_civil
    WHERE ID_Locador = p_id_locador;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION excluir_locador(
    p_id_locador INTEGER
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Locador WHERE ID_Locador = p_id_locador;
END;
$$ LANGUAGE plpgsql;





CREATE OR REPLACE FUNCTION criar_estado_civil(
    p_desc_estado_civil VARCHAR
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Estado_Civil (Desc_Estado_Civil)
    VALUES (p_desc_estado_civil);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION editar_estado_civil(
    p_id_estado_civil INTEGER,
    p_desc_estado_civil VARCHAR
) RETURNS VOID AS $$
BEGIN
    UPDATE Estado_Civil
    SET Desc_Estado_Civil = p_desc_estado_civil
    WHERE ID_Estado_Civil = p_id_estado_civil;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION excluir_estado_civil(
    p_id_estado_civil INTEGER
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Estado_Civil WHERE ID_Estado_Civil = p_id_estado_civil;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION criar_locatario(
    p_nome VARCHAR,
    p_telefone VARCHAR,
    p_rg VARCHAR,
    p_cpf_cnpj VARCHAR,
    p_id_estado_civil INTEGER
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Locatario (Nome, Telefone, RG, CPF_CNPJ, ID_Estado_Civil)
    VALUES (p_nome, p_telefone, p_rg, p_cpf_cnpj, p_id_estado_civil);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION editar_locatario(
    p_id_locatario INTEGER,
    p_nome VARCHAR,
    p_telefone VARCHAR,
    p_rg VARCHAR,
    p_cpf_cnpj VARCHAR,
    p_id_estado_civil INTEGER
) RETURNS VOID AS $$
BEGIN
    UPDATE Locatario
    SET Nome = p_nome, Telefone = p_telefone, RG = p_rg, CPF_CNPJ = p_cpf_cnpj, ID_Estado_Civil = p_id_estado_civil
    WHERE ID_Locatario = p_id_locatario;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION excluir_locatario(
    p_id_locatario INTEGER
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Locatario WHERE ID_Locatario = p_id_locatario;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION criar_forma_pagamento(desc_forma_pgto TEXT)
RETURNS VOID AS $$
BEGIN
    INSERT INTO forma_pagamento (desc_forma_pgto)
    VALUES (desc_forma_pgto);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION editar_forma_pagamento(id_forma_pagamento INT, desc_forma_pgto TEXT)
RETURNS VOID AS $$
BEGIN
    UPDATE forma_pagamento
    SET desc_forma_pgto = desc_forma_pgto
    WHERE id_forma_pagamento = id_forma_pagamento;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION excluir_forma_pagamento(id_forma_pagamento INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM forma_pagamento
    WHERE id_forma_pagamento = id_forma_pagamento;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION listar_formas_pagamento()
RETURNS TABLE(id_forma_pagamento INT, desc_forma_pgto TEXT) AS $$
BEGIN
    RETURN QUERY SELECT * FROM forma_pagamento;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION criar_pagamento(
    p_dt_paga DATE,
    p_ref_mes_ano VARCHAR,
    p_observacao VARCHAR,
    p_id_contrato INTEGER,
    p_id_locatario INTEGER,
    p_id_forma_pagamento INTEGER
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Registro_Pagamento (DT_Paga, Ref_Mes_Ano, Observacao, ID_Contrato, ID_Locatario, ID_Forma_Pagamento)
    VALUES (p_dt_paga, p_ref_mes_ano, p_observacao, p_id_contrato, p_id_locatario, p_id_forma_pagamento);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION editar_pagamento(
    p_id_pagamento INTEGER,
    p_dt_paga DATE,
    p_ref_mes_ano VARCHAR,
    p_observacao VARCHAR,
    p_id_contrato INTEGER,
    p_id_locatario INTEGER,
    p_id_forma_pagamento INTEGER
) RETURNS VOID AS $$
BEGIN
    UPDATE Registro_Pagamento
    SET DT_Paga = p_dt_paga, Ref_Mes_Ano = p_ref_mes_ano, Observacao = p_observacao, ID_Contrato = p_id_contrato, ID_Locatario = p_id_locatario, ID_Forma_Pagamento = p_id_forma_pagamento
    WHERE ID_Pagamento = p_id_pagamento;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION excluir_pagamento(
    p_id_pagamento INTEGER
) RETURNS VOID AS $$
BEGIN
    DELETE FROM Registro_Pagamento WHERE ID_Pagamento = p_id_pagamento;
END;
$$ LANGUAGE plpgsql;
