from db_funcoes import fn_validacao,fn_inserir_ordem,apaga_banco

apaga_banco()
fn_inserir_ordem('A','ABEV3' ,      'C', 500, 11.14)
fn_inserir_ordem('O','ABEVD126',    'V', 500, 0.11,     12.00)

fn_inserir_ordem('A','BBDC4',       'C', 500, 11.78)
fn_inserir_ordem('O','BBDCC126',    'V', 500, 0.15,     12.32)
fn_inserir_ordem('O','BBDCC126',    'C', 500, 0.15)
fn_inserir_ordem('O','BBDCD125',    'V', 500, 0.35,     12.52)

fn_inserir_ordem('A','CSAN3' ,      'C', 600, 7.27)
fn_inserir_ordem('O','CSANC840',    'V', 600, 0.08,     8.40)
fn_inserir_ordem('O','CSAND820',    'V', 600, 0.13,     8.20)

fn_inserir_ordem('A','CYRE3' ,      'C', 100, 21.79)
fn_inserir_ordem('A','CYRE3' ,      'V', 100, 21.00)
fn_inserir_ordem('O','CYREC210' ,   'V', 100, 1.33,     21.00)

fn_inserir_ordem('A','EQTL3' ,      'C', 100, 30.95)
fn_inserir_ordem('A','EQTL3' ,      'V', 100, 30.07)
fn_inserir_ordem('O','EQTLC301' ,   'V', 100, 1.50,     30.07)

fn_inserir_ordem('A','HAPV3' ,      'C', 2000, 2.18)
fn_inserir_ordem('O','HAPVC265' ,   'V', 2000, 0.02,     2.65)
fn_inserir_ordem('O','HAPVD245' ,   'V', 2000, 0.06,     2.45)

