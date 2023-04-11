CREATE CONSTRAINT cons_user_ukey      IF NOT EXISTS ON (u:User) ASSERT u.id IS UNIQUE ;
CREATE CONSTRAINT cons_email_ukey      IF NOT EXISTS ON (e:Email) ASSERT e.msg_id IS UNIQUE ;
// CREATE CONSTRAINT cons_email_ukey     IF NOT EXISTS ON (e:Email) ASSERT (e.msg_id, n.id) IS NODE KEY ;
show constraints;
