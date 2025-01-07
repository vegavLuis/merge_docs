import { exec } from "child_process";
import path from "path";

const comando = `python combinar_doc.py "${path.resolve(
  "archivo2.docx"
)}" "${path.resolve("archivo1.docx")}" "${path.resolve(
  "documento_combinado.docx"
)}"`;

exec(comando, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error al ejecutar el comando: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`Error en stderr: ${stderr}`);
    return;
  }
  console.log(stdout);
});
