function(doc) {
  if (doc.key_id) {
    // emit(doc.key_id, doc);
    emit(doc.key_id, {"valid_from": doc.valid_from, "valid_to": doc.valid_to});
  }
}
