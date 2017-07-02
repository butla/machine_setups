bootstrap:
	pip3 install --user ansible
	@bash -c 'if ! command -v ansible > /dev/null; then echo "Ansible isn'\''t on the PATH, add ~/.local/bin to it"; else echo Ansible is set up; fi'

run:
	ANSIBLE_NOCOWS=1 ansible-playbook main_machine.yml -i localhost --ask-become-pass
